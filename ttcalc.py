#!/usr/bin/env python
__author__ = 'ioparaskev'

from trainings.saba_trainings import SabaTrainingTimer
from trainings.trainings import TrainingTimeCalculator
from argparse import ArgumentParser


def args_crafter():

    parser = ArgumentParser(prog='ttcalc',
                            description='Total training time calculator.'
                                        'Calculates total training time based '
                                        'on csv file import',
                            usage='%(prog)s [options]')
    parser.add_argument('-f', '--file', help='CSV file to open for parsing '
                                             'the trainings')
    parser.add_argument('-e', '--exclude', help='File that contains '
                                                'in each line the name for '
                                                'training to exclude')
    parser.add_argument('-d', '--delimiter', help='Change the delimiter for '
                                                  'splitting csv columns',
                        default='|', type=str)
    parser.add_argument('-T', '--title', help='The column number for the '
                                              'title of the trainings',
                        default=0, type=int)
    parser.add_argument('-t', '--time', help='The column number for the '
                                             'time of the trainings',
                        default=3, type=int)
    return parser


def options_are_customized(delimiter, time_num, title_num):
    if not (delimiter == '|' and title_num == 0 and time_num == 3):
        return True
    else:
        return False


def main():
    parse = args_crafter()
    args_parse = parse.parse_args()
    file_name = args_parse.file
    exclude_file = args_parse.exclude

    delimiter = args_parse.delimiter
    title_num = args_parse.title
    time_num = args_parse.time
    custom = options_are_customized(delimiter, time_num, title_num)

    timer_constructor = TrainingTimeCalculator if custom else SabaTrainingTimer

    print('\n*******Training time counter*******')
    if not file_name:
        print('Make sure the file is in the same folder with this script,\n'
              'otherwise you will have to enter the full path\n')
        file_name = input('Enter file name with the file extension: ')

    if not exclude_file:
        exclude_file = input('\nEnter file name with trainings to exclude\n'
                             '(Press enter if there\'s no such file): ')

    try:
        mbb40 = timer_constructor(file_name, exclude_file)
        mbb40.setup_options(delimiter, title_num, time_num)
        print()
        mbb40.autorun()
    except IndexError:
        print('Error parsing file! Make sure that delimiter and '
              'title/time column options are correct')
    except Exception as error:
        print(error)
    finally:
        print()
        input('Press any key to exit')

if __name__ == '__main__':
    main()
