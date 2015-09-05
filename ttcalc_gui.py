__author__ = 'jparaske'

from tkinter import ttk, filedialog, messagebox, font
import tkinter as tkint
from trainings.saba_trainings import SabaTrainingTimer
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
        for w in range(0, maxwidth+1, 5):
            if self.winfo_reqwidth() >= pixels:
                break
            self.config(width=width+w)


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

        self.training_calculator_cls = SabaTrainingTimer

        self.mbb40 = None

    def _setup_buttons(self, frame):
        csv_file_button = tkint.Button(frame, text='Open file with trainings',
                                       command=self._set_training_file, width=50)
        csv_file_button.pack()
        exclude_file_button = tkint.Button(frame, text='Open file with exclusions',
                                           command=self._set_exclusions_file, width=50)
        exclude_file_button.pack()
        quit_button = tkint.Button(self, text="Quit", command=self.parent.destroy)
        quit_button.pack(side=tkint.RIGHT, padx=5, pady=5)
        ok_button = tkint.Button(self, text="Run", command=self.run)
        ok_button.pack(side=tkint.RIGHT)

        clear_button = tkint.Button(self, text="Clear", command=self._clear)
        clear_button.pack(side=tkint.LEFT, padx=5, pady=5)

        options_button = tkint.Button(self, text="Options", command=self.__options)
        options_button.pack(side=tkint.LEFT, padx=5, pady=5)

    def _setup_ui(self):

        self.parent.title("SABA Training time calculator")

        frame = tkint.Frame(self, relief=tkint.RAISED, borderwidth=1)
        frame.pack(fill=tkint.BOTH, expand=1)
        self.pack(fill=tkint.BOTH, expand=1)

        self._setup_buttons(frame)

    def _set_training_file(self):
        self.csv_file_name = tkint.filedialog.askopenfilename()

    def _set_exclusions_file(self):
        self.exlusions_file_name = tkint.filedialog.askopenfilename()

    def _setup_new_window(self, title=''):
        self.popup = tkint.Toplevel(self)
        self.popup.wm_title(title)
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

        time_label = tkint.Label(self.popup, text='{} hours {} minutes {} seconds'
                                 .format(*results[1]))
        time_label.pack()
        close_button = tkint.Button(self.popup, text="Close",
                                    command=self.popup.destroy)
        close_button.pack(side=tkint.RIGHT, padx=5, pady=5)
        self.listbox.autowidth(600)
        center(self.popup)

    def _exclude(self):
        exclusions = [int(x) for x in self.listbox.curselection()]
        self.mbb40.exclude(exclusions)
        results = self.mbb40.gui_report()
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

    def __options(self):
        self._setup_new_window('CSV import file options')

    def run(self):
        if not self.csv_file_name:
            tkint.messagebox.showerror('Error', 'No csv file given!')
            return

        self.mbb40 = self.training_calculator_cls(self.csv_file_name,
                                                  self.exlusions_file_name)

        results = self.mbb40.gui_report()

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
    if platform == "win32":
        root.iconbitmap('{}\chronometer.ico'
                        .format(path.dirname(path.realpath(__file__))))
    else:
        img = tkint.Image("photo", file="chronometer.gif")
        root.tk.call('wm', 'iconphoto', root._w, img)
    root.mainloop()


if __name__ == '__main__':
    main()
