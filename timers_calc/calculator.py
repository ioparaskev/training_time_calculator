__author__ = 'ioparaskev'

import datetime
from timers_calc.hms import TimeCalculator


class TimestampTimeCalculator(TimeCalculator):
    def __init__(self, trainings):
        self.trainings = trainings
        super(TimestampTimeCalculator, self).__init__(0)

    def get_time_delta(self, training):
        times = training.timestamp.split(":")
        if len(times) > 2:
            return times
        elif len(times) < 2:
            return 0, 0, int(times[0])
        else:
            return int(times[0]), int(times[1]), 0

    def _total_time_sum(self):
        total_time = datetime.timedelta(hours=0, minutes=0)
        for train in self.trainings:
            try:
                hour, minutes, seconds = self.get_time_delta(train)
                total_time += datetime.timedelta(hours=hour,
                                                 minutes=minutes,
                                                 seconds=seconds)
            except ValueError:
                continue

        return total_time

    def calculate_total_training_time(self):
        self._seconds = self._total_time_sum().total_seconds()
        return self.calculate()
