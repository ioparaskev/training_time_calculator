__author__ = 'ioparaskev'

import csv
from file_handlers.generic_file import FileReader


class CSVReader(FileReader):
    def __init__(self, file_name, delimiter=',', newline=''):
        super(CSVReader, self).__init__(file_name, newline)
        self._delimeter = delimiter

    @property
    def delimiter(self):
        return self._delimeter

    def read_file(self):
        read_columns = []
        with self.open_file() as file:
            line_reader = csv.reader(file, delimiter='|')
            for row in line_reader:
                read_columns.append(row)

        return tuple(read_columns)


class CSVKeywordSkipper(object):
    def __init__(self):
        self._skip_keywords = dict()

    def set_skip_keywords(self, keywords=None):
        self._skip_keywords = keywords

    def keep_row(self, row):
        keywords = self._skip_keywords
        for i, column in enumerate(row):
            if str(i) in keywords and keywords[str(i)] in column:
                return False
        return True

    def skip_rows_by_keywords(self, rows):
        non_skipped_rows = []

        for row in rows:
            if self.keep_row(row):
                non_skipped_rows.append(row)

        return non_skipped_rows