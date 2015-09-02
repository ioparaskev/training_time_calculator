#!/usr/bin/env python
__author__ = 'ioparaskev'

import csv
import datetime
import os.path
import logging
from prompt_handles import PromptWrapper


class CSVReader(object):
    def __init__(self, file_name, delimiter=',', newline=''):
        try:
            self.validate_file_name(file_name)
            self.file_name = file_name
            self.__delimiter = delimiter
            self.__new_line = newline
            self.__skip_keywords = dict()
        except RuntimeError:
            logging.error('Invalid file name or file does not exist')
            raise RuntimeError('Invalid file name or file does not exist')

    def validate_file_name(self, file_name):
        if not (os.path.exists(file_name) and os.path.isfile(file_name)):
            raise RuntimeError()

    def set_skip_keywords_in_columns(self, keywords_in_columns=None):
        self.__skip_keywords = keywords_in_columns

    @property
    def delimiter(self):
        return self.__delimiter

    @property
    def new_line(self):
        return self.__new_line

    def open_file(self):
        return open(self.file_name, 'r', newline=self.new_line)

    def skip_line(self, row):
        if not (self.__skip_keywords and isinstance(self.__skip_keywords, dict)) :
            return False

        for i, entry in enumerate(row):
            skip_keyword = self.__skip_keywords.get(str(i), '')
            if skip_keyword and skip_keyword in entry:
                return True

        return False

    def read_file(self):
        read_columns = []
        with self.open_file() as file:
            line_reader = csv.reader(file, delimiter='|')
            for row in line_reader:
                try:
                    if self.skip_line(row):
                        continue
                    read_columns.append(row)
                except IndexError:
                    continue
        return tuple(read_columns)


class TimeCalculator(object):
    def __init__(self, secs):
        self.hours = 0
        self.minutes = 0
        self.seconds = secs

    def set_hours_minutes_seconds(self, hours, minutes, seconds):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    @property
    def h_m_s(self):
        return self.hours, self.minutes, self.seconds

    def hours_minute_secs_calculator(self):
        hours, remainder = divmod(self.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return hours, minutes, seconds

    def calculate(self):
        self.set_hours_minutes_seconds(*self.hours_minute_secs_calculator())


class Training(object):
    def __init__(self, title, timestamp):
        self.title = title
        self.timestamp = timestamp


class TrainingTimeCalculator(object):
    def __init__(self, trainings):
        self.trainings = trainings


class MBB40H(object):
    def __init__(self, file_name):
        try:
            self.csv_reader = CSVReader(file_name, delimiter='|', newline='')
        except RuntimeError as err:
            print(err)
            exit(1)

        column_keywords_to_skip = {"0": "Item Name",
                                   "1": "Status",
                                   "2": "Marked Complete By",
                                   "3": "Duration(HH:MM)"}
        self.csv_reader.set_skip_keywords_in_columns(column_keywords_to_skip)
        self.total_time = TimeCalculator(0)
        self.__trainings = tuple()

    def calculate_total_time(self, trainings):
        total_time = datetime.timedelta(hours=0, minutes=0)

        for train in trainings:
            timer = datetime.datetime.strptime(train.timestamp, '%H:%M')
            total_time += datetime.timedelta(hours=timer.hour, minutes=timer.minute)

        self.total_time = TimeCalculator(total_time.total_seconds())
        self.total_time.calculate()

    def print_training_titles(self):
        print('*******Training titles*******')
        for i, train in enumerate(self.__trainings):
            print('#{num}  {title}'.format(num=i+1, title=train.title))

    def print_total_training_time(self):
        hours, minutes, seconds = self.total_time.h_m_s
        print('\n*******Total time of training*******'
              '\n{} hours {} minutes {} seconds'.format(hours, minutes, seconds))

    def craft_training(self, line):
        training = Training(title=line[0], timestamp=line[3])
        return training

    def create_trainings(self):
        exported_trainings = self.csv_reader.read_file()
        trainings = []

        for line in exported_trainings:
            trainings.append(self.craft_training(line))

        self.__trainings = tuple(trainings)

    def calculate_trainings(self):
        if not self.__trainings:
            self.create_trainings()

        self.calculate_total_time(self.__trainings)
        self.print_training_titles()
        self.print_total_training_time()

    @staticmethod
    def setup_exclude_prompt():
        exclude_question = 'Do you want to exclude? (y=yes, n=no, q=quit)'
        exclude_answers = ('y', 'n', 'q')
        prompt = PromptWrapper(exclude_question, exclude_answers)
        return prompt

    def exclude_training(self, training):
        self.__trainings = tuple(train for train in self.__trainings if train is not training)

    def exclude(self):
        prompt = self.setup_exclude_prompt()

        for training in self.__trainings:
            print(training.title)
            choice = prompt.get_prompt_answer().lower()

            if choice == 'y':
                self.exclude_training(training)
            elif choice == 'n':
                continue
            elif choice == 'q':
                break
        print("\n\n\n\n")
        self.calculate_trainings()


def main():
    print('*******Training time counter*******\n\n')
    print('Make sure the file is in the same folder with this script,\n'
          'otherwise you will have to enter the full path\n')
    file_name = input('Enter file name with the file extension:')

    mbb40 = MBB40H(file_name)
    mbb40.calculate_trainings()

    exclude_question = 'Do you want to exclude any of the trainings? (y/n)'
    exclude_answers = ('y', 'n')
    prompt = PromptWrapper(exclude_question, exclude_answers)
    exclude_choice = prompt.get_prompt_answer()

    if exclude_choice == 'y':
        mbb40.exclude()


if __name__ == '__main__':
    main()
