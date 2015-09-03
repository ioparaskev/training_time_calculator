__author__ = 'ioparaskev'


class TimeCalculator(object):
    def __init__(self, secs):
        self._seconds = secs

    @staticmethod
    def hours_minute_secs_calculator(seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return hours, minutes, seconds

    def calculate(self):
        return self.hours_minute_secs_calculator(self._seconds)