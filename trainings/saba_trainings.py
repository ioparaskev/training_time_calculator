__author__ = 'ioparaskev'

from file_handlers.csv import CSVKeywordSkipper
from trainings.trainings import TrainingTimeCalculator


class SabaTrainingTimer(TrainingTimeCalculator):
    def _setup_exclusions(self):
        self.keyword_skipper = CSVKeywordSkipper()
        column_keywords_to_skip = {"0": "Item Name",
                                   "1": "Status",
                                   "2": "Marked Complete By",
                                   "3": "Duration(HH:MM)"}
        self.keyword_skipper.set_skip_keywords(column_keywords_to_skip)

    def __init__(self, file_name, exclude_file=None):
        super(SabaTrainingTimer, self).__init__(file_name, exclude_file)
        self._setup_exclusions()
        self.title_column_num = 0
        self.time_column_num = 3
