__author__ = 'ioparaskev'

from file_handlers.csv import CSVReader, CSVKeywordSkipper
from prompt_handler.prompt_handles import PromptWrapper
from trainings.trainings import TrainingsPoolFilter, SabaTrainings


class SabaTrainingTimer(object):
    def _setup_exclusions(self):
        self.keyword_skipper = CSVKeywordSkipper()
        column_keywords_to_skip = {"0": "Item Name",
                                   "1": "Status",
                                   "2": "Marked Complete By",
                                   "3": "Duration(HH:MM)"}
        self.keyword_skipper.set_skip_keywords(column_keywords_to_skip)

    def __init__(self, file_name, exclude_file=None):
        self.keyword_skipper = None
        self.exclude_file = exclude_file
        self.csv_reader = CSVReader(file_name, delimiter='|', newline='')

        self._setup_exclusions()
        self.total_time = tuple()
        self.training_pool = None

    def _create_trainings(self):
        lines = self.csv_reader.read_file()
        exported_trainings = self.keyword_skipper.skip_rows_by_keywords(lines)
        self.training_pool = SabaTrainings(exported_trainings)

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
