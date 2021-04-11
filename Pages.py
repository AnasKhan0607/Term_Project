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
https://stackoverflow.com/questions/13828531/problems-in-python-getting-multiple-selections-from-tkinter-listbox
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

        self.sub_btn = Button(self, text='Submit', command=lambda: parent.change_frame(PageTwo, "Hello"))
        self.sub_btn.grid(row=2, column=1)
        self.sub_btn["state"] = DISABLED

        self.pack()
        # If a game option is selected call the callback function
        self.game_choices.bind("<<ComboboxSelected>>", self.callback)

    def callback(self, event_object):
        self.game = event_object.widget.get()
        if self.game != "Select a game":
            self.sub_btn["state"] = NORMAL




class PageTwo(tk.Frame):
    """
    For Overwatch
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        parent.title('Statistical Tracker for: Overwatch')
        tk.Label(self, text="Player information:").grid(row=0, column=0, columnspan=2)
        self.num_players = 0

        self.parent = parent


        self.ow_tree = ttk.Treeview(self)
        # Create the columns
        self.ow_tree['columns'] = ("Battle Tag", "Platform", "Region")
        self.ow_tree.column("#0", width=120, minwidth=25)
        self.ow_tree.column("Battle Tag", anchor=W, width=120)
        self.ow_tree.column("Platform", anchor=CENTER, width=80)
        self.ow_tree.column("Region", anchor=W, width=60)
        # Create the headings
        self.ow_tree.heading("#0", text="Player #", anchor=W)
        self.ow_tree.heading("Battle Tag", text="Battle Tag", anchor=CENTER)
        self.ow_tree.heading("Platform", text="Platform", anchor=W)
        self.ow_tree.heading("Region", text="Region", anchor=CENTER)

        self.ow_tree.grid(row=0, column=2, rowspan=5, padx=5, pady=5, sticky=E + W + S + N)

        self.platform_chosen = StringVar()
        self.region_chosen = StringVar()
        self.battle_id = StringVar()

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

        self.battle_id.trace("w", lambda name, index, mode, new_id=self.battle_id: self.validate_tag(new_id))
        self.gamer_tag = Entry(self, textvariable=self.battle_id)

        self.gamer_tag.grid(row=4, column=1)

        self.add_btn = Button(self, text='Add Player', command=self.add_player)
        self.add_btn.grid(row=0, column=4)
        self.add_btn = Button(self, text='Remove Player(s)', command=self.validate_tag)
        self.add_btn.grid(row=1, padx=5, column=4)
        self.add_btn = Button(self, text='Clear', command=self.clear)
        self.add_btn.grid(row=2, column=4)
        self.back_btn = Button(self, text='Go back', command=lambda: parent.change_frame(PageOne)).grid(row=3, column=4)
        self.sub_btn = Button(self, text='Submit', command=lambda: parent.change_frame(PageThree)).grid(row=4, column=4)


    def validate_tag(self, id):
        if "#" in id.get():
            self.battle_id.set(self.battle_id.get().replace("#", "-"))

    def add_player(self):

        try:
            o = Overwatch(self.platform_chosen.get(), self.region_chosen.get(), self.battle_id.get())

            if o.result:
                if not self.parent.game_filters:
                    self.parent.game_filters = o.get_filters()
                    self.parent.displayed_stats = o.displayed_filters


                self.num_players += 1
                self.parent.all_players.extend([o])

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
        self.parent = parent

        self.Label_Stats = Label(self, text='Choose at least two stats to compare')
        self.Label_Stats.grid(row=0, column=1, columnspan = 2)

        self.gameplay = StringVar()
        self.qp_btn = Radiobutton(self, text ="Quick Play", variable = self.gameplay, value = "quickPlayStats", command = lambda: self.gameplay_chosen(), tristatevalue=0)
        self.cp_btn = Radiobutton(self, text="Competitive", variable=self.gameplay, value="competitiveStats", command=lambda: self.gameplay_chosen(), tristatevalue=0)



        self.qp_btn.grid(row = 1, column = 1)
        self.cp_btn.grid(row = 1, column = 2)

        self.scrollbar = Scrollbar(self, orient = VERTICAL)
        self.scrollbar.grid(row=2, column=2, sticky=tk.N + tk.S)
        self.filter_list = self.parent.displayed_stats



        self.filter_lb = Listbox(self, selectmode = MULTIPLE, width = 50, yscrollcommand=self.scrollbar.set)
        for filter in self.filter_list[1:]:
            self.filter_lb.insert(END, filter)
        self.filter_lb.grid(row = 2, column = 1, sticky=tk.N + tk.S + tk.E + tk.W)
        self.filter_lb["state"] = DISABLED
        self.filter_lb.bind("<<ListboxSelect>>", self.selected_stats)
        self.scrollbar['command'] = self.filter_lb.yview

        self.sbt_stats = Button(self, text='Submit', command=lambda: parent.change_frame(PageFour))
        self.sbt_stats.grid(row=3, column=1)
        self.sbt_stats["state"] = DISABLED

    def selected_stats(self, lb):
        selected_stats = lb.widget.curselection()
        self.parent.compared_stats = ["Name"]
        if (selected_stats != ()):
            for stat in selected_stats:

                if self.filter_list[int(stat)+1] not in self.parent.compared_stats:
                    self.parent.compared_stats.append(self.filter_list[int(stat) + 1])
        if len(self.parent.compared_stats) >= 2:
            self.sbt_stats["state"] = NORMAL
        else:
            self.sbt_stats["state"] = DISABLED



    def gameplay_chosen(self):
        self.filter_lb["state"] = NORMAL
        self.parent.game_mode = self.gameplay.get()



class PageFour(tk.Frame):
    """
    The Fourth page
    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.compared_players = self.parent.all_players
        self.compared_stats = self.parent.compared_stats
        self.Label_table = Label(self, text='Table')
        self.Label_table.grid(row=0, column=1, columnspan=2)
        self.tree_stats = {}

        self.sub_awards = {'Cards': 'cards', 'Medals': 'medals', 'Bronze Medals': 'medalsBronze', 'Silver Medals': 'medalsSilver',
                 'Gold Medals': 'medalsGold'}
        self.sub_game_results = {'Games Won':'gamesWon', 'gamesLost':'gamesLost', 'gamesPlayed':'gamesPlayed'}
        self.in_game_stats = {'barrierDamageDone': 'barrierDamageDone', 'damageDone': 'damageDone', 'deaths': 'deaths',
                              'eliminations': 'eliminations','soloKills': 'soloKills','objectiveKills': 'objectiveKills'}
        self.best_game_results = {'allDamageDoneMostInGame': 'allDamageDoneMostInGame', 'barrierDamageDoneMostInGame':'barrierDamageDoneMostInGame', 'eliminationsMostInGame':'eliminationsMostInGame',
                                  'healingDoneMostInGame':'healingDoneMostInGame', 'killsStreakBest':'killsStreakBest', 'multikillsBest':'multikillsBest'}
        self.in_game_index = 0
        self.best_in_game_index = 0
        self.game_outcome_index = 0
        self.awards_index = 0







        for stat in self.parent.compared_stats:
            self.tree_stats[stat] = []
            self.get_player_info(stat)

        self.ow_stat_tree = ttk.Treeview(self)
        # Create the columns
        self.ow_stat_tree['columns'] = self.tree_stats['Name']


        self.ow_stat_tree.column("#0", width=120, minwidth=25)
        #
        for x, stat in enumerate(self.tree_stats['Name']):

            self.ow_stat_tree.column(x, anchor=CENTER, width=100)

        # Create the headings
        self.ow_stat_tree.heading("#0", text="Player #", anchor=W)
        for x, stat in enumerate(self.tree_stats['Name']):
            self.ow_stat_tree.heading(x, text="Player {}".format(x+1), anchor=CENTER)
        self.ow_stat_tree.grid(row=0, column=2, rowspan=len(self.tree_stats['Name']) + 1, padx=5, pady=5, sticky=E + W + S + N)



        for x, stat in enumerate(self.tree_stats):
            """
            Create this in the parent class as attribute
            """
            if stat == 'In-Game Stats':
                self.in_game_index = x
                self.ow_stat_tree.insert('', index='end', iid=x, text=stat)
            elif stat == 'Best In-Game Stats':
                self.best_in_game_index = x
                self.ow_stat_tree.insert('', index='end', iid=x, text=stat)
            elif stat == 'Game Outcomes':
                self.game_outcome_index = x
                self.ow_stat_tree.insert('', index='end', iid=x, text=stat)
            elif stat == 'Awards':
                self.awards_index = x
                self.ow_stat_tree.insert('', index='end', iid=x, text=stat)
            elif stat in self.sub_awards:
                self.ow_stat_tree.insert('', index='end', iid=x, text=stat, values = self.tree_stats[stat])
                self.ow_stat_tree.move(str(x), str(self.awards_index), str(self.awards_index))
            elif stat in self.best_game_results:
                self.ow_stat_tree.insert('', index='end', iid=x, text=stat, values = self.tree_stats[stat])
                self.ow_stat_tree.move(str(x), str(self.best_in_game_index), str(self.best_in_game_index))
            elif stat in self.in_game_stats:
                self.ow_stat_tree.insert('', index='end', iid=x, text=stat, values = self.tree_stats[stat])
                self.ow_stat_tree.move(str(x), str(self.in_game_index), str(self.in_game_index))
            elif stat in self.sub_game_results:
                self.ow_stat_tree.insert('', index='end', iid=x, text=stat, values = self.tree_stats[stat])
                self.ow_stat_tree.move(str(x), str(self.game_outcome_index), str(self.game_outcome_index))
            else:
                self.ow_stat_tree.insert('', index='end', iid=x, text=stat, values = self.tree_stats[stat])

    # self.displayed_filters = ['Name', 'Level', 'Prestige', 'Rating', 'Endorsement Level', 'In-Game Stats',
    #                           'Best In-Game Stats', 'Game Outcomes', 'Awards']
    # self.api_filters.extend(
    #     ['name', 'level', 'prestige', 'rating', 'Endorsement Level', 'In-Game Stats', 'Best In-Game Stats',
    #      'Game Outcomes', 'Awards'])
    def get_player_info(self, stat):

        for player in self.compared_players:
            if stat == 'Awards':
                sub_awards = self.sub_awards
                for sub_stat in sub_awards:
                    if sub_stat not in self.tree_stats:
                        self.tree_stats[sub_stat] = []
                    self.tree_stats[sub_stat].append(player.get_stat(sub_awards[sub_stat], self.parent.game_mode))
            elif stat == 'Game Outcomes':
                sub_game_results = self.sub_game_results
                for sub_stat in sub_game_results:
                    if sub_stat not in self.tree_stats:
                        self.tree_stats[sub_stat] = []
                    self.tree_stats[sub_stat].append(player.get_stat(sub_game_results[sub_stat], self.parent.game_mode))
            elif stat == 'In-Game Stats':
                in_game_stats = self.in_game_stats
                for sub_stat in in_game_stats:
                    if sub_stat not in self.tree_stats:
                        self.tree_stats[sub_stat] = []
                    self.tree_stats[sub_stat].append(player.get_stat(in_game_stats[sub_stat], self.parent.game_mode))
            elif stat == 'Best In-Game Stats':
                best_game_results = self.best_game_results
                for sub_stat in best_game_results:
                    if sub_stat not in self.tree_stats:
                        self.tree_stats[sub_stat] = []
                    self.tree_stats[sub_stat].append(player.get_stat(best_game_results[sub_stat], self.parent.game_mode))
            else:
                self.tree_stats[stat].append(player.get_stat(stat, self.parent.game_mode))







