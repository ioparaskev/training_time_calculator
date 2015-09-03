#!/usr/bin/env python
__author__ = 'ioparaskev'

from trainings.saba_trainings import SabaTrainingTimer


def main():
    print('*******Training time counter*******\n\n')
    print('Make sure the file is in the same folder with this script,\n'
          'otherwise you will have to enter the full path\n')
    file_name = input('Enter file name with the file extension: ')
    exclude_file = input('\nEnter file name with trainings to exclude\n'
                         '(Press enter if there\'s no such file): ')

    try:
        mbb40 = SabaTrainingTimer(file_name, exclude_file)
        mbb40.autorun()
    except Exception as error:
        print(error)

if __name__ == '__main__':
    main()
