from tkinter import *
from tkinter import ttk
import tkinter as tk
from Pages import PageOne
from apicollect import Overwatch

class FirstGUI(tk.Tk):
    """
    This is pertaining to Overwatch only, Remember that in the apicollect.py file,
    Overwatch API requires you to put in platform, region and battle id of the player.
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Statistical Tracker for:")
        self._frame = None
        self.change_frame(PageOne)

    def change_frame(self, change_frame):
        new_frame = change_frame(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()



if __name__ == "__main__":
    app = FirstGUI()
    app.mainloop()