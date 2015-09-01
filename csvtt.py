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
            raise

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

    def read_file(self):
        return open(self.file_name, self.new_line)

    def skip_line(self, row):
        if not (self.__skip_keywords and isinstance(dict, self.__skip_keywords)) :
            return False

        for column in row:
            skip_keyword = self.__skip_keywords.get([column], '')
            if skip_keyword and column.find(skip_keyword) != -1:
                return True
        return False

    def read_column(self, column_num):
        read_columns = []
        with self.read_file() as file:
            line_reader = csv.reader(file, delimiter='|')
            for row in line_reader:
                if self.skip_line(row):
                    continue


class MBB40H(object):
    pass


def main():
    print('*******Training time counter*******\n\n')
    print('Make sure the file is in the same folder with this script,\n'
          'otherwise you will have to enter the full path\n')
    file_name = input('Enter file name with the file extension:')

    with open(file_name, newline='') as csv_file:
        line_reader = csv.reader(csv_file, delimiter='|')
        add_time = datetime.timedelta(hours=0, minutes=0)
        for row in line_reader:
            print(row[0])
            if row[3].find('Duration') != -1:
                continue
            timer = datetime.datetime.strptime(row[3], '%H:%M')
            add_time += datetime.timedelta(hours=timer.hour, minutes=timer.minute)
        hours, remainder = divmod(add_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        print('Total time of csv')
        print('{} hours {} minutes {} seconds'.format(int(hours), int(minutes), int(seconds)))


if __name__ == '__main__':
    main()

#todo add functions for moduling
    #todo time column should be variable not constant
    #todo escaping of lines with no duration should be more agile
    #todo support for automatic selection of entries to count & skip
#todo add unit tests



