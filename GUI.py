from tkinter import *
from tkinter import ttk
from apicollect import Overwatch


class FirstGUI:
    """
    This is pertaining to Overwatch only, Remember that in the apicollect.py file,
    Overwatch API requires you to put in platform, region and battle id of the player.
    """
    def __init__(self, parent):
        self.parent = parent
        self.game = None

        self.frame = Frame(self.parent)
        self.labelSelect = Label(self.frame, text='Choose a game to find stats to compare between multiple players')
        self.labelSelect.grid(row=0, column=1)
        self.game_chosen = StringVar()
        # Create a dropdown menu
        self.game_choices = ttk.Combobox(self.frame, state="readonly", textvariable=self.game_chosen, width=30)
        # Default text shown
        self.game_choices.set("Select a game")
        # Possible games to choose from: Cold war and WoW are examples for now
        self.game_choices['values'] = ['Overwatch', 'Fortnite', 'Cold War', 'WoW']
        self.game_choices.grid(row=1, column=1)

        """
        Idea: Maybe we can use validate commands for the entries
        """
        # Entry for user to put in platform

        # platform_label_text = StringVar()
        # platform_label_text.set("Enter game platform (pc, etc)")
        # self.label1 = Label(app, textvariable=platform_label_text, height=4)
        # self.label1.grid(row=2, column=0)

        platform_id = StringVar()
        self.first_gamer_plat = Entry(self.frame, textvariable=platform_id)
        self.first_gamer_plat.grid(row=2, column=1)

        # Entry for user to put in region

        # region_label_text = StringVar()
        # region_label_text.set("Enter game region (us, eu, asia)")
        # self.label2 = Label(app, textvariable=region_label_text, height=4)
        # self.label2.grid(row=3, column=0)

        region_id = StringVar()
        self.first_gamer_reg = Entry(self.frame, textvariable=region_id)
        self.first_gamer_reg.grid(row=3, column=1)

        # Entry for user to put in battle_id

        # battleID_label_text = StringVar()
        # battleID_label_text.set("Your battlenet tag, replacing the # with a -")
        # self.label3 = Label(app, textvariable=battleID_label_text, height=4)
        # self.label3.grid(row=3, column=0)

        battle_id = StringVar()
        self.first_gamer_batt = Entry(self.frame, textvariable=battle_id)
        self.first_gamer_batt.grid(row=4, column=1)

        # Submit Button
        self.sub_btn = Button(self.frame, text='Submit', command=self.submit)
        self.sub_btn.grid(row=5, column=3)

        self.frame.pack()
        # If a game option is selected call the callbackf function
        self.game_choices.bind("<<ComboboxSelected>>", self.callback)

    def callback(self, event_object):
        self.game = event_object.widget.get()

    def submit(self):
        """
        Retrieve the values from each entry and check if they are valid.
        """
        platform = self.first_gamer_plat.get()
        region = self.first_gamer_reg.get()
        battle_tag = self.first_gamer_batt.get()

        try:
            o = Overwatch(platform, region, battle_tag)
            if o.result:
                # Simple check to see if values are valid
                print(o.test_get_player_info())
            else:
                print("Invalid Profile")
        except:
            # Need to likely change this try/except. Debugging required
            print("Invalid Profile")


app = Tk()
gui = FirstGUI(app)
app.title("Game App")
app.geometry('500x600')
app.mainloop()
