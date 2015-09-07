from file_handlers.csv import CSVReader

__author__ = 'ioparaskev'

from copy import copy
from file_handlers.generic_file import FileReader
from prompt_handler.prompt_handles import PromptWrapper
from timers_calc.calculator import TimestampTimeCalculator


class Training(object):
    def __init__(self, title, timestamp):
        self.title = title
        self.timestamp = timestamp


class TrainingsPool(object):
    def __init__(self, trainings_stack):
        self._trainings = tuple(self._craft_training(entry)
                                for entry in trainings_stack)
        self._total_training_time = (0, 0, 0)

    @property
    def trainings(self):
        return [x for x in self._trainings]

    def training_exists(self, training):
        for x in self._trainings:
            if x.title == training.title:
                return True
        return False

    def remove_training(self, training):
        if self.training_exists(training):
            self._trainings = tuple(x for x in self._trainings
                                    if x.title != training.title)
        self._total_training_time = (0, 0, 0)

    @property
    def training_time(self):
        return self._total_training_time

    @property
    def _time_not_set(self):
        return filter(lambda x: x != 0, self.training_time)

    @staticmethod
    def _craft_training(entry):
        training = Training(title=entry[0], timestamp=entry[1])
        return training

    def print_training_titles(self):
        print('\n-------Training titles-------')
        for i, train in enumerate(self._trainings):
            print('#{num}  {title}'.format(num=i+1, title=train.title))

    def print_total_training_time(self):
        print('\n*******Total time of trainings*******'
              '\n{} hours {} minutes {} seconds\n'.format(*self.training_time))

    def calculate_training_time(self):
        training_time = TimestampTimeCalculator(self._trainings)
        return training_time.calculate_total_training_time()

    def setup_time(self):
        if self._time_not_set:
            self._total_training_time = self.calculate_training_time()

    def print_report(self):
        self.setup_time()
        self.print_training_titles()
        self.print_total_training_time()

    def get_report(self):
        self.setup_time()
        return self._trainings, self.training_time


class TrainingPoolCrafter(TrainingsPool):
    def __init__(self, title_column_num, time_column_num, extracted_trainings):
        trainings_stack = [[x[title_column_num], x[time_column_num]]
                           for x in extracted_trainings]
        super(TrainingPoolCrafter, self).__init__(trainings_stack)


class TrainingsPoolFilter(object):
    def __init__(self, traing_pool, exclude_file=None):
        self.training_pool = copy(traing_pool)
        self.exclude_reader = FileReader(exclude_file) if exclude_file else None

    @staticmethod
    def _setup_exclude_prompt():
        exclude_question = 'Do you want to exclude? (y=yes, n=no, q=quit)'
        exclude_answers = ('y', 'n', 'q')
        prompt = PromptWrapper(exclude_question,
                               accepted_answers=exclude_answers)
        return prompt

    def _exclude_training(self, training):
        self.training_pool.remove_training(training)

    def _exclude_multiple_trainings(self, training_stack):
        for training in training_stack:
            self._exclude_training(training)

    def _exclude_interactively(self):
        prompt = self._setup_exclude_prompt()
        for training in self.training_pool.trainings:
            print(training.title)
            choice = prompt.get_prompt_answer().lower()
            if choice == 'y':
                self._exclude_training(training)
            elif choice == 'n':
                continue
            elif choice == 'q':
                break

    def _exclude_from_file(self):
        exclusions = [[x, 0] for x in self.exclude_reader.read_file()]
        trainings_to_exclude = TrainingsPool(exclusions)
        self._exclude_multiple_trainings(trainings_to_exclude.trainings)

    def filter_trainings(self, trainings=None):
        if trainings:
            for i, training in enumerate(self.training_pool.trainings):
                if i in trainings:
                    self._exclude_training(training)
        elif not self.exclude_reader:
            self._exclude_interactively()
        else:
            self._exclude_from_file()

        return self.training_pool


class TrainingTimeCalculator(object):
    def __init__(self, file_name, exclude_file):
        self.exclude_file = exclude_file
        self.total_time = tuple()
        self.csv_reader = CSVReader(file_name, delimiter='|', newline='')
        self.title_column_num = 0
        self.time_column_num = 0
        self.keyword_skipper = None
        self.training_pool = None

    def _create_trainings(self):
        lines = self.csv_reader.read_file()
        if self.keyword_skipper:
            lines = self.keyword_skipper.skip_rows_by_keywords(lines)
        self.training_pool = TrainingPoolCrafter(self.title_column_num,
                                                 self.time_column_num,
                                                 lines)

    def _setup_training_pool(self):
        if not self.training_pool:
            self._create_trainings()

    def print_report(self):
        self._setup_training_pool()
        self.training_pool.print_report()

    def _filter_trainings(self, trainings=None):
        training_filter = TrainingsPoolFilter(self.training_pool, self.exclude_file)
        return training_filter.filter_trainings(trainings)

    def _interactive_exclusion(self):
        exclude_question = 'Do you want to exclude any of the trainings?(y/n)'
        exclude_answers = ('y', 'n')
        prompt = PromptWrapper(exclude_question,
                               accepted_answers=exclude_answers)
        exclude_choice = prompt.get_prompt_answer()
        return exclude_choice == 'y'

    def exclude(self, exclusions=None):
        filtered_pool = self._filter_trainings(exclusions)
        if len(filtered_pool.trainings) != len(self.training_pool.trainings):
            self.training_pool = filtered_pool

    def autorun(self):
        self._setup_training_pool()
        if self.exclude_file or self._interactive_exclusion():
            self.exclude()
        self.print_report()

    def get_report(self):
        return self.training_pool.get_report()

    def gui_report(self):
        self._setup_training_pool()
        if self.exclude_file:
            self.exclude()
        return self.get_report()