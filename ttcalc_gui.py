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

    @property
    def _training_crafter(self):
        return SabaTrainingTimer

    @property
    def training_calculator(self):
        if not self._calculator:
            self._calculator = self._training_crafter(self.csv_file_name,
                                                      self.exlusions_file_name)

        return self._calculator

    def _setup_buttons(self, frame):
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

        # options_button = tkint.Button(self, text="Options",
        #                               command=self.__options)
        # options_button.pack(side=tkint.LEFT, padx=5, pady=5)

        about_button = tkint.Button(self, text="About", command=self.__about)
        about_button.pack(side=tkint.LEFT, padx=5, pady=5)

    def _setup_ui(self):

        self.parent.title("Training time calculator")

        frame = tkint.Frame(self, relief=tkint.RAISED, borderwidth=1)
        frame.pack(fill=tkint.BOTH, expand=1)
        self.pack(fill=tkint.BOTH, expand=1)

        self._setup_buttons(frame)

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

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):

        pass

    def __options(self):
        self._setup_new_window('CSV import file options')

        delimiter_label = tkint.Label(self.popup, text='Column delimiter:')
        delimiter_label.pack(side=tkint.LEFT)

        vcmd = (self.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        delimiter_text = tkint.Text('')
        delimiter_text.pack()



        close_button = tkint.Button(self.popup, text="Close",
                                    command=self.popup.destroy)
        close_button.pack(side=tkint.RIGHT, padx=5, pady=5)

        save_button = tkint.Button(self.popup, text="Save",
                                   command=self.popup.destroy)
        save_button.pack(side=tkint.RIGHT, padx=5, pady=5)

        center(self.popup)

    def run(self):
        if not self.csv_file_name:
            tkint.messagebox.showerror('Error', 'No csv file given!')
            return

        results = self.training_calculator.gui_report()

        if self.exlusions_file_name:
            self._show_results(results)
        else:
            self._show_results_to_exclude(results)


def main():
    root = tkint.Tk()
    root.geometry("300x100+200+100")
    root.resizable(0, 0)
    mbb40Gui(root)
    center(root)
    root.mainloop()


if __name__ == '__main__':
    main()
