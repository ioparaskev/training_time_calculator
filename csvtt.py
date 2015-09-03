#!/usr/bin/env python
from file_handlers import CSVReader, CSVKeywordSkipper
from prompt_handles import PromptWrapper
from trainings import TrainingsPool, TrainingFilter


__author__ = 'ioparaskev'


class MBB40H(TrainingFilter):
    def _setup_exclusions(self):
        self.keyword_skipper = CSVKeywordSkipper()
        column_keywords_to_skip = {"0": "Item Name",
                                   "1": "Status",
                                   "2": "Marked Complete By",
                                   "3": "Duration(HH:MM)"}
        self.keyword_skipper.set_skip_keywords(column_keywords_to_skip)

    def __init__(self, file_name, exclude_file=None):
        self.keyword_skipper = None
        self.exclude_reader = None
        try:
            self.csv_reader = CSVReader(file_name, delimiter='|', newline='')
            if exclude_file:
                super(MBB40H, self).__init__(exclude_file)
        except RuntimeError as err:
            print(err)
            exit(1)

        self._setup_exclusions()
        self.total_time = tuple()
        self.training_pool = None

    def _create_trainings(self):
        lines = self.csv_reader.read_file()
        exported_trainings = self.keyword_skipper.skip_rows_by_keywords(lines)
        self.training_pool = TrainingsPool(exported_trainings)

    def print_report(self):
        if not self.training_pool:
            self._create_trainings()
        self.training_pool.print_report()


def main():
    print('*******Training time counter*******\n\n')
    print('Make sure the file is in the same folder with this script,\n'
          'otherwise you will have to enter the full path\n')
    file_name = input('Enter file name with the file extension: ')
    exclude_file = input('\nEnter file name with trainings to exclude\n'
                         '(Press enter if there\'s no such file): ')

    mbb40 = MBB40H(file_name, exclude_file)
    mbb40.print_report()

    exclude_question = 'Do you want to exclude any of the trainings? (y/n)'
    exclude_answers = ('y', 'n')
    prompt = PromptWrapper(exclude_question, exclude_answers)
    exclude_choice = prompt.get_prompt_answer()

    if exclude_choice == 'y':
        mbb40.exclude()


if __name__ == '__main__':
    main()
