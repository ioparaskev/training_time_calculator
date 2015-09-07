__author__ = 'ioparaskev'

import datetime
from timers_calc.hms import TimeCalculator


class TimestampTimeCalculator(TimeCalculator):
    def __init__(self, trainings, time_format='%H:%M'):
        self.trainings = trainings
        self.time_format = time_format
        super(TimestampTimeCalculator, self).__init__(0)

    def _total_time_sum(self):
        total_time = datetime.timedelta(hours=0, minutes=0)
        for train in self.trainings:
            try:
                timer = datetime.datetime.strptime(train.timestamp,
                                                   self.time_format)
                total_time += datetime.timedelta(hours=timer.hour,
                                                 minutes=timer.minute)
            except ValueError:
                continue

        return total_time

    def calculate_total_training_time(self):
        self._seconds = self._total_time_sum().total_seconds()
        return self.calculate()