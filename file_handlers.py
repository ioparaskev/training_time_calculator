import csv
import logging
import os.path

__author__ = 'jparaske'


class FileReader(object):
    def __init__(self, file_name, newline=''):
        try:
            self.validate_file_name(file_name)
        except RuntimeError:
            logging.error('Invalid file name or file does not exist')
            raise RuntimeError('Invalid file name or file does not exist')

        self.file_name = file_name
        self._new_line = newline

    @staticmethod
    def validate_file_name(file_name):
        if not (os.path.exists(file_name) and os.path.isfile(file_name)):
            raise RuntimeError()

    @property
    def new_line(self):
        return self._new_line

    def open_file(self):
        return open(self.file_name, 'r', newline=self.new_line)

    def read_file(self):
        with self.open_file() as file:
            read_lines = file.readlines()
        return read_lines


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


class FileKeywordSkipper(object):
    def __init__(self):
        self._skip_keywords = None

    def set_skip_keywords(self, keywords=None):
        self._skip_keywords = set(keywords)

    def skip_lines_by_keywords(self, lines):
        non_skipped_lines = lines[:]
        for line in lines:
            if self._skip_keywords & set(line.split()):
                non_skipped_lines.remove(line)

        return non_skipped_lines


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