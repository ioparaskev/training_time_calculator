__author__ = 'jparaske'

from tkinter import ttk, filedialog, messagebox, font
import tkinter as tkint
from trainings.saba_trainings import SabaTrainingTimer
from trainings.trainings import TrainingTimeCalculator
from os import path
from sys import platform


def center(toplevel):
    toplevel.withdraw()
    toplevel.update_idletasks()  # Update "requested size" from geometry manager

    x = (toplevel.winfo_screenwidth() - toplevel.winfo_reqwidth()) // 2
    y = (toplevel.winfo_screenheight() - toplevel.winfo_reqheight()) // 2
    toplevel.geometry("+{}+{}".format(x, y))

    # This seems to draw the window frame immediately, so only call deiconify()
    # after setting correct window position
    toplevel.deiconify()


class ResizableListbox(tkint.Listbox):
    def autowidth(self, maxwidth):
        f = font.Font(font=self.cget("font"))
        pixels = 0
        for item in self.get(0, "end"):
            pixels = max(pixels, f.measure(item))
        # bump listbox size until all entries fit
        pixels = pixels + 10
        width = int(self.cget("width"))
        for w in range(0, maxwidth + 1, 5):
            if self.winfo_reqwidth() >= pixels:
                break
            self.config(width=width + w)


class mbb40Gui(tkint.Frame):
    def __init__(self, parent):
        tkint.Frame.__init__(self, parent)

        self.parent = parent
        self.style = tkint.ttk.Style()
        self.style.theme_use("clam")
        self._setup_ui()

        self.listbox = None
        self.popup = None

        self.csv_file_name = None
        self.exlusions_file_name = None

        self._calculator = None

        self.delimiter = '|'
        self.title_column = 0
        self.time_column = 3

        self.custom_options = None

    @property
    def _training_crafter(self):
        if self.custom_options:
            return TrainingTimeCalculator
        return SabaTrainingTimer

    @property
    def training_calculator(self):
        if not self._calculator:
            self._calculator = self._training_crafter(self.csv_file_name,
                                                      self.exlusions_file_name)
            self._calculator.setup_options(self.delimiter, self.title_column,
                                           self.time_column)

        return self._calculator

    def _setup_main_window_buttons(self, frame):
        csv_file_button = tkint.Button(frame, text='Open file with trainings',
                                       command=self._set_training_file,
                                       width=50)
        csv_file_button.pack()
        exclude_file_button = tkint.Button(frame,
                                           text='Open file with exclusions',
                                           command=self._set_exclusions_file,
                                           width=50)
        exclude_file_button.pack()
        quit_button = tkint.Button(self, text="Quit",
                                   command=self.parent.destroy)
        quit_button.pack(side=tkint.RIGHT, padx=5, pady=5)
        ok_button = tkint.Button(self, text="Run", command=self.run)
        ok_button.pack(side=tkint.RIGHT)

        clear_button = tkint.Button(self, text="Clear", command=self._clear)
        clear_button.pack(side=tkint.LEFT, padx=5, pady=5)

        options_button = tkint.Button(self, text="Options",
                                      command=self.__options)
        options_button.pack(side=tkint.LEFT, padx=5, pady=5)

        about_button = tkint.Button(self, text="About", command=self.__about)
        about_button.pack(side=tkint.LEFT, padx=5, pady=5)

    def _setup_ui(self):

        self.parent.title("Training time calculator")

        frame = tkint.Frame(self, relief=tkint.RAISED, borderwidth=1)
        frame.pack(fill=tkint.BOTH, expand=1)
        self.pack(fill=tkint.BOTH, expand=1)

        self._setup_main_window_buttons(frame)

    def _set_training_file(self):
        types = [('CSV files', '*.csv')]
        self.csv_file_name = tkint.filedialog.askopenfilename(filetypes=types)

    def _set_exclusions_file(self):
        types = [('Text files', '*.txt'), ('All files', '*')]
        self.exlusions_file_name = tkint.filedialog.askopenfilename(filetypes=types)

    def _setup_new_window(self, title='', geometry=None):
        self.popup = tkint.Toplevel(self)
        self.popup.wm_title(title)
        if geometry:
            self.popup.geometry(geometry)
        frame = tkint.Frame(self.popup, relief=tkint.RAISED, borderwidth=1)
        frame.pack(fill=tkint.BOTH, expand=True)
        self.popup.grab_set()

    def _setup_results_window(self, total_entries):
        self._setup_new_window("Trainings done #{0}".format(total_entries))

    def _list_results(self, results):
        self._setup_results_window(len(results[0]))
        self.listbox = ResizableListbox(self.popup, height=20, width=70,
                                        selectmode="extended")
        self.listbox.pack(fill=tkint.BOTH, expand=True)
        for i, training in enumerate(results[0]):
            self.listbox.insert(i, "   {}".format(training.title))

        time_label = tkint.Label(self.popup,
                                 text='{} hours {} minutes {} seconds'
                                 .format(*results[1]))
        time_label.pack()
        close_button = tkint.Button(self.popup, text="Close",
                                    command=self.popup.destroy)
        close_button.pack(side=tkint.RIGHT, padx=5, pady=5)
        self.listbox.autowidth(600)
        center(self.popup)

    def _exclude(self):
        exclusions = [int(x) for x in self.listbox.curselection()]
        self.training_calculator.exclude(exclusions)
        results = self.training_calculator.gui_report()
        self.popup.destroy()
        self._show_results(results)

    def _show_results_to_exclude(self, results):
        self._list_results(results)
        exclude_button = tkint.Button(self.popup, text="Exclude",
                                      command=self._exclude)
        exclude_button.pack(side=tkint.RIGHT)

    def _show_results(self, results):
        self._list_results(results)

    def _clear(self):
        self.csv_file_name = None
        self.exlusions_file_name = None
        self._calculator = None
        self.custom_options = None

    def __about(self):
        self._setup_new_window('About Training time Calculator')

        __help = ('Open csv file to open for parsing the trainings\n'
                   'Create a txt file containing on each line the training'
                   'to exclude, to automatically exclude those trainings\n'
                   'Originally developed for Nokia SABA trainings calculation\n'
                   'Developed by: John Paraskevopoulos\n'
                   'MIT License - 2015'
                   '')
        help_text = tkint.Text(self.popup, height=8, wrap=tkint.WORD)
        help_text.pack(side=tkint.TOP)
        help_text.insert(tkint.END, __help)
        help_text.config(state=tkint.DISABLED)

        close_button = tkint.Button(self.popup, text="Close",
                                    command=self.popup.destroy)
        close_button.pack(side=tkint.RIGHT, padx=5, pady=5)
        center(self.popup)

    def validate_num(self, action, char, post_val, pro_val, text, t_validation,
                     validation, widget_name):

        if not text.isdigit() or len(post_val) > 5:
            self.bell()
            return False
        return True

    def validate_delimiter(self, action, char, post_val, pro_val, text, t_validation,
                     validation, widget_name):
        if not text.isprintable() or len(post_val) > 1:
            self.bell()
            return False
        return True

    def __save(self):
        self._calculator = None
        self.delimiter = self.custom_options['delimiter'].get()
        title_num = self.custom_options['title'].get()
        if title_num:
            self.title_column = int(title_num)
        else:
            self.title_column = 0

        time_num = self.custom_options['time'].get()
        if time_num:
            self.time_column = int(time_num)
        else:
            self.time_column = 0

        self.popup.destroy()

    def _create_custom_csv_options(self):
        delimiter_label = tkint.Label(self.popup, text='Column delimiter:')
        delimiter_label.pack(side=tkint.LEFT)

        validate_delimiter = (self.register(self.validate_delimiter),
                              '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        delimiter_text = tkint.Entry(self.popup, validate="key",
                                     validatecommand=validate_delimiter,
                                     width=1)
        delimiter_text.pack(side=tkint.LEFT, padx=5)
        delimiter_text.delete(0, tkint.END)
        delimiter_text.insert(0, self.delimiter)

        validate_num = (self.register(self.validate_num),
                        '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        title_label = tkint.Label(self.popup, text='Title column #:')
        title_label.pack(side=tkint.LEFT)

        title_num = tkint.Entry(self.popup, validate="key", text=self.title_column,
                                validatecommand=validate_num, width=5)
        title_num.delete(0, tkint.END)
        title_num.insert(0, self.title_column)
        title_num.pack(side=tkint.LEFT, padx=5)

        time_label = tkint.Label(self.popup, text='Time column #:')
        time_label.pack(side=tkint.LEFT)

        time_num = tkint.Entry(self.popup, validate="key",
                               validatecommand=validate_num, width=5)

        time_num.delete(0, tkint.END)
        time_num.insert(0, self.time_column)
        time_num.pack(side=tkint.LEFT, padx=5)

        self.custom_options = {'delimiter': delimiter_text, 'title': title_num,
                               'time': time_num}

    def __options(self):
        self._setup_new_window('CSV import file options')

        self._create_custom_csv_options()

        close_button = tkint.Button(self.popup, text="Close",
                                    command=self.popup.destroy)
        close_button.pack(side=tkint.RIGHT, padx=5, pady=5)

        save_button = tkint.Button(self.popup, text="Save",
                                   command=self.__save)
        save_button.pack(side=tkint.RIGHT, padx=5, pady=5)

        center(self.popup)

    def run(self):
        if not self.csv_file_name:
            tkint.messagebox.showerror('Error', 'No csv file given!')
            return

        try:
            results = self.training_calculator.gui_report()

            if self.exlusions_file_name:
                self._show_results(results)
            else:
                self._show_results_to_exclude(results)
        except IndexError:
            parse_error = ('Error parsing file! Make sure that delimiter and '
                           'title/time column options are correct')
            tkint.messagebox.showerror('Error parsing file', parse_error)
            return

def main():
    root = tkint.Tk()
    root.geometry("380x100+200+100")
    root.resizable(0, 0)
    mbb40Gui(root)
    center(root)
    root.mainloop()


if __name__ == '__main__':
    main()
