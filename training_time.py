__author__ = 'jparaske'

import datetime


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


class TimestampTimeCalculator(TimeCalculator):
    def __init__(self, trainings, time_format='%H:%M'):
        self.trainings = trainings
        self.time_format = time_format
        super(TimestampTimeCalculator, self).__init__(0)

    def _total_time_sum(self):
        total_time = datetime.timedelta(hours=0, minutes=0)
        for train in self.trainings:
            timer = datetime.datetime.strptime(train.timestamp, self.time_format)
            total_time += datetime.timedelta(hours=timer.hour, minutes=timer.minute)

        return total_time

    def calculate_total_training_time(self):
        self._seconds = self._total_time_sum().seconds
        return self.calculate()


class Training(object):
    def __init__(self, title, timestamp):
        self.title = title
        self.timestamp = timestamp


class TrainingsPool(object):
    def __init__(self, trainings_stack):
        self._trainings = tuple(self._craft_training(entry)
                                for entry in trainings_stack)
        self._total_training_time = (0, 0, 0)

    @property
    def trainings(self):
        return [x for x in self._trainings]

    def remove_training(self, training):
        if training in self._trainings:
            self._trainings = tuple(train for train in self._trainings
                                    if train is not training)
        self._total_training_time = (0, 0, 0)

    @property
    def training_time(self):
        return self._total_training_time

    @property
    def _time_not_set(self):
        return filter(lambda x: x != 0, self.training_time)

    @staticmethod
    def _craft_training(line):
        training = Training(title=line[0], timestamp=line[3])
        return training

    def print_training_titles(self):
        print('*******Training titles*******')
        for i, train in enumerate(self._trainings):
            print('#{num}  {title}'.format(num=i+1, title=train.title))

    def print_total_training_time(self):
        print('\n*******Total time of trainings*******'
              '\n{} hours {} minutes {} seconds'.format(*self.training_time))

    def calculate_training_time(self):
        training_time = TimestampTimeCalculator(self._trainings)
        return training_time.calculate_total_training_time()

    def print_report(self):
        if self._time_not_set:
            self._total_training_time = self.calculate_training_time()

        self.print_training_titles()
        self.print_total_training_time()
