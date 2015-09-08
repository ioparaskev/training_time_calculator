# training_time_calculator
CSV import based training time calculator. Originally developed for Nokia SABA training time calculations, but expanded to more generic options and handling. Time must be in HH:MM format

### ttcalc (console version)
  * Optional arguments
    * `-f, --file: csv file to open for parsing the trainings`
    * `-e, --exclude: file that contains on each line the name for the training to exclude`
    * `-h, --help: help`
    * `-d, --delimiter: Change the delimiter for splitting csv columns`
    * `-T, --title: The column number for the title of the trainings`
    * `-t, --time: The column number for the time of the trainings`

### ttcalc_gui (gui version)
  * Run button calculates the trainings
    * New window gives the choice to exclude trainings (if no exclude file was given)
  * Options allow the setup for the csv import options (delimiter to use, which number is the delimetered column containings the times)
