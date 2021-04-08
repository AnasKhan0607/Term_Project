from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from apicollect import Overwatch

"""
Sources:
https://www.youtube.com/watch?v=YTqDYmfccQU
https://www.delftstack.com/howto/python-tkinter/how-to-switch-frames-in-tkinter/
https://www.youtube.com/watch?v=7JoMTQgdxg0
"""


class PageOne(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.game = None
        self.labelSelect = Label(self, text='Choose a game to find stats to compare between multiple players')
        self.labelSelect.grid(row=0, column=1)
        self.game_chosen = StringVar()
        # Create a dropdown menu
        self.game_choices = ttk.Combobox(self, state="readonly", textvariable=self.game_chosen, width=30)
        # Default text shown
        self.game_choices.set("Select a game")
        # Possible games to choose from: Cold war and WoW are examples for now
        self.game_choices['values'] = ['Overwatch', 'Fortnite', 'Cold War', 'WoW']
        self.game_choices.grid(row=1, column=1)

        """
        Idea: Maybe we can use validate commands for the entries
        """

        self.sub_btn = Button(self, text='Submit', command=lambda: self.testing(parent)).grid(
            row=2, column=1)
        # self.sub_btn.grid(row=5, column=3)

        self.pack()
        # If a game option is selected call the callback function
        self.game_choices.bind("<<ComboboxSelected>>", self.callback)

    def callback(self, event_object):
        self.game = event_object.widget.get()

    def testing(self, parent):
        if self.game_choices.get() != "Select a game":
            parent.change_frame(PageTwo)


class PageTwo(tk.Frame):
    """
    For Overwatch
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        parent.title('Statistical Tracker for: Overwatch')
        tk.Label(self, text="Player information:").grid(row=0, column=0, columnspan=2)
        self.num_players = 0

        # self.all_players = []

        self.ow_tree = ttk.Treeview(self)
        # Create the columns
        self.ow_tree['columns'] = ("Battle Tag", "Platform", "Region")
        self.ow_tree.column("#0", width=120, minwidth=25)
        self.ow_tree.column("Battle Tag", anchor=W, width=120)
        self.ow_tree.column("Platform", anchor=CENTER, width=80)
        self.ow_tree.column("Region", anchor=W, width=60)
        # Create the headings
        self.ow_tree.heading("#0", text="Label", anchor=W)
        self.ow_tree.heading("Battle Tag", text="Battle Tag", anchor=CENTER)
        self.ow_tree.heading("Platform", text="Platform", anchor=W)
        self.ow_tree.heading("Region", text="Region", anchor=CENTER)

        # Add Data
        # ow_tree.insert('', index='end', iid=0, text="Player", values=("Yash", "pc", "us"))

        self.ow_tree.grid(row=0, column=2, rowspan=5, padx=5, pady=5, sticky=E + W + S + N)

        self.platform_chosen = StringVar()
        self.region_chosen = StringVar()
        self.battletag_chosen = StringVar()

        tk.Label(self, text="Player 1").grid(row=1, column=0, columnspan=2)

        tk.Label(self, text="Platform:").grid(row=2, column=0, columnspan=1)
        # Create a dropdown menu
        self.platform_choices = ttk.Combobox(self, state="readonly", textvariable=self.platform_chosen, width=30)
        # Default text shown
        self.platform_choices.set("Select a platform")
        # Possible platforms to choose
        self.platform_choices['values'] = ['pc', 'xbl', 'psn']
        self.platform_choices.grid(row=2, column=1)

        tk.Label(self, text="Region:").grid(row=3, column=0, columnspan=1)
        # Create a dropdown menu
        self.region_choices = ttk.Combobox(self, state="readonly", textvariable=self.region_chosen, width=30)
        # Default text shown
        self.region_choices.set("Select a region")
        # Possible regions to choose
        self.region_choices['values'] = ['us', 'eu', 'kr', 'cn', 'global']
        self.region_choices.grid(row=3, column=1)

        tk.Label(self, text="Battle Tag:").grid(row=4, column=0, columnspan=1)

        self.battle_id = StringVar()
        self.gamer_tag = Entry(self, textvariable=self.battle_id)
        self.gamer_tag.grid(row=4, column=1)
        window = tk.Tk()

        self.add_btn = Button(self, text='Add Player', command=self.add_player)
        self.add_btn.grid(row=0, column=4)
        self.add_btn = Button(self, text='Remove Player(s)', command=self.remove_players)
        self.add_btn.grid(row=1, padx=5, column=4)
        self.add_btn = Button(self, text='Clear', command=self.clear)
        self.add_btn.grid(row=2, column=4)
        self.back_btn = Button(self, text='Go back', command=lambda: parent.change_frame(PageOne)).grid(row=3, column=4)
        self.sub_btn = Button(self, text='Submit', command=lambda: parent.change_frame(PageThree)).grid(row=4, column=4)

    def add_player(self):

        try:
            o = Overwatch(self.platform_chosen.get(), self.region_chosen.get(), self.battle_id.get())
            if o.result:
                self.num_players += 1
                self.ow_tree.insert('', index='end', iid=self.num_players, text="Player {}".format(self.num_players),
                                    values=(self.battle_id.get(), self.platform_chosen.get(), self.region_chosen.get()))

                self.gamer_tag.delete(0, END)
                self.platform_choices.set('Select a platform')
                self.region_choices.set('Select a region')
            else:
                messagebox.showinfo('Error!', 'You have entered an invalid profile!')

        except:
            messagebox.showinfo('Error!', 'You have entered an invalid profile!')

    def clear(self):
        for player in self.ow_tree.get_children():
            self.ow_tree.delete(player)

    def remove_players(self):
        t = self.ow_tree.selection()
        for player in t:
            self.ow_tree.delete(player)


class PageThree(tk.Frame):
    """
    The Third page
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Input the player").grid(row=0, column=1, columnspan=2)
