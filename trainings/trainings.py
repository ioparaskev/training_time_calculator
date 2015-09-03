__author__ = 'ioparaskev'

from copy import deepcopy
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
        print('\n*******Training titles*******')
        for i, train in enumerate(self._trainings):
            print('#{num}  {title}'.format(num=i+1, title=train.title))

    def print_total_training_time(self):
        print('\n*******Total time of trainings*******'
              '\n{} hours {} minutes {} seconds\n'.format(*self.training_time))

    def calculate_training_time(self):
        training_time = TimestampTimeCalculator(self._trainings)
        return training_time.calculate_total_training_time()

    def print_report(self):
        if self._time_not_set:
            self._total_training_time = self.calculate_training_time()

        self.print_training_titles()
        self.print_total_training_time()


class SabaTrainings(TrainingsPool):
    def __init__(self, extracted_trainings):
        trainings_stack = [[x[0], x[3]] for x in extracted_trainings]
        super(SabaTrainings, self).__init__(trainings_stack)


class TrainingsPoolFilter(object):
    def __init__(self, traing_pool, exclude_file=None):
        self.training_pool = deepcopy(traing_pool)
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

    def filter_trainings(self):
        if not self.exclude_reader:
            self._exclude_interactively()
        else:
            self._exclude_from_file()

        return self.training_pool
