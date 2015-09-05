#!/usr/bin/env python
__author__ = 'ioparaskev'

from trainings.saba_trainings import SabaTrainingTimer
from argparse import ArgumentParser


def args_crafter():

    parser = ArgumentParser(prog='mbb40',
                            description='SABA total training time counter',
                            usage='%(prog)s [options]')
    parser.add_argument('-f', '--file', help='CSV file to open for parsing '
                                             'the trainings')
    parser.add_argument('-e', '--exclude', help='File that contains '
                                                'in each line the name for '
                                                'training to exclude')
    return parser


def main():
    parse = args_crafter()
    args_parse = parse.parse_args()
    file_name = args_parse.file
    exclude_file = args_parse.exclude

    print('\n*******Training time counter*******')
    if not file_name:
        print('Make sure the file is in the same folder with this script,\n'
              'otherwise you will have to enter the full path\n')
        file_name = input('Enter file name with the file extension: ')

    if not exclude_file:
        exclude_file = input('\nEnter file name with trainings to exclude\n'
                             '(Press enter if there\'s no such file): ')

    try:
        mbb40 = SabaTrainingTimer(file_name, exclude_file)
        mbb40.autorun()
    except Exception as error:
        print(error)
    finally:
        input('Press any key to exit')

if __name__ == '__main__':
    main()
