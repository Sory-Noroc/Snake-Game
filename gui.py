
import tkinter
import sys


class StarterGui:
    def __init__(self, context):
        self.context = context
        self.mw = tkinter.Tk()  # The main window
        self.mw.title('Snake')  # It's title
        self.mw.configure(bg='yellow')  # The background

        # Main window positioning
        self.x = self.mw.winfo_screenwidth() // 4
        self.y = self.mw.winfo_screenheight() // 4
        self.mw_width = self.mw.winfo_screenwidth() // 2
        self.mw_height = self.mw.winfo_screenheight() // 2
        self.mw.geometry(f'{self.mw_width}x{self.mw_height}+{self.x}+{self.y}')

    def lobby(self):
        for child in self.mw.winfo_children():  # The clearing mechanism before the lobby initialization
            child.destroy()  # Clears all the widgets

        title = tkinter.StringVar(self.mw)  # The name of the game
        title.set('Snake')
        title_label = tkinter.Label(self.mw, justify='center', textvariable=title, fg='darkblue', bg='yellow',
                                    anchor='center', font='Arial 60', padx=0, pady=0)  # The name of the game
        settings_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', width=30,
                                         text='Settings', command=self.settings)
        play_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', text='Play',
                                     justify='center', width=30, command=self.context.game_loop)
        exit_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', text='Exit',
                                     justify='center', width=30, command=sys.exit)

        # Placing all the widgets of the lobby
        title_label.place(x=220, y=50)
        play_button.place(x=220, y=160)
        exit_button.place(x=220, y=240)
        settings_button.place(x=220, y=200)
        self.mw.mainloop()  # GUI mainloop

    def settings(self):
        for child in self.mw.winfo_children():  # Clears the interface
            child.destroy()

        choose_diff_text = tkinter.StringVar(self.mw)
        choose_diff_text.set('Choose difficulty')
        difficulty_label = tkinter.Label(self.mw, justify='center', textvariable=choose_diff_text, fg='blue',
                                         bg='yellow', anchor='center', font='Arial 20', padx=0, pady=0)
        easy_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', width=6,
                                     text='Easy', command=self.easy)
        medium_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', width=6,
                                       text='Medium', command=self.medium)
        expert_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', width=6,
                                       text='Expert', command=self.expert)
        return_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', width=6,
                                       text='Return', command=self.lobby)
        exit_button = tkinter.Button(self.mw, activebackground='lightblue', bg='lightgray', fg='blue', width=6,
                                     text='Exit', command=sys.exit)

        # PLacing the widgets of the Setting tab
        difficulty_label.place(x=240, y=100)
        easy_button.place(x=180, y=140)
        medium_button.place(x=320, y=140)
        expert_button.place(x=460, y=140)
        return_button.place(x=280, y=300)
        exit_button.place(x=360, y=300)

    def easy(self):  # Difficulty
        self.context.difficulty = 10

    def medium(self):
        self.context.difficulty = 25

    def expert(self):
        self.context.difficulty = 50
