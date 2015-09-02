#!/usr/bin/env python

import datetime

from file_handlers import FileReader, CSVReader, CSVKeywordSkipper
from prompt_handles import PromptWrapper
from training_time import TrainingsPool


__author__ = 'ioparaskev'


class MBB40H(object):
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
                self.exclude_reader = FileReader(exclude_file)
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

    @staticmethod
    def setup_exclude_prompt():
        exclude_question = 'Do you want to exclude? (y=yes, n=no, q=quit)'
        exclude_answers = ('y', 'n', 'q')
        prompt = PromptWrapper(exclude_question, exclude_answers)
        return prompt

    def exclude_training(self, training):
        self.training_pool.remove_training(training)

    def exclude(self):
        prompt = self.setup_exclude_prompt()

        for training in self.training_pool.trainings:
            print(training.title)
            choice = prompt.get_prompt_answer().lower()

            if choice == 'y':
                self.exclude_training(training)
            elif choice == 'n':
                continue
            elif choice == 'q':
                break
        print('\n\n\n\n')
        self.print_report()

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
