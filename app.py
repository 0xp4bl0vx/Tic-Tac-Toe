import customtkinter
import core
from functools import partial
from random import choice
from PIL import Image

CROSS = 1
CIRCLE = -1

HUMAN_PLAYER = -1
AI_PLAYER = 1


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.game = None
        self.result = None
        self.ai_player = None
        self.player_order = None
        self.geometry("500x500")
        self.title("Tic Tac Toe")
        self.buttons = [customtkinter.CTkButton(self, width=156, height=156, text="", image=None,
                                                command=partial(self.button_click, i)) for i in range(9)]
        self.restart_button = customtkinter.CTkButton(self, width=150, height=40, text="Jugar otra vez",
                                                      command=self.restart)
        self.end_text = customtkinter.CTkLabel(self, text="", font=("Helvetica", 26))
        self.two_player_button = customtkinter.CTkButton(self, width=200, height=60, text="Jugador vs Jugador",
                                                         font=("Helvetica", 18), command=self.two_players)
        self.algorithm_player_button = customtkinter.CTkButton(self, width=200, height=60,
                                                               command=self.algorithm_player,
                                                               text="Jugador vs Algoritmo", font=("Helvetica", 18))
        self.title_label = customtkinter.CTkLabel(self, text="Tic Tac Toe", font=("Helvetica", 34))
        self.select_mode_label = customtkinter.CTkLabel(self, text="Elige el modo de juego:", font=("Helvetica", 26))
        self.choose_first_player = customtkinter.CTkLabel(self, text="Elige quién empieza:", font=("Helvetica", 30))
        self.ai_first_button = customtkinter.CTkButton(self, width=200, height=60, text="Jugador IA",
                                                       command=self.ai_button, font=("Helvetica", 18))
        self.player_first_button = customtkinter.CTkButton(self, width=200, height=60, text="Yo",
                                                           command=self.player_button, font=("Helvetica", 18))
        self.random_player_button = customtkinter.CTkButton(self, width=200, height=60, text="Aleatorio",
                                                            command=self.random_button, font=("Helvetica", 18))
        self.x_image = customtkinter.CTkImage(Image.open("assets/cross.png"), size=(125, 125))
        self.o_image = customtkinter.CTkImage(Image.open("assets/circle.png"), size=(125, 125))
        self.start_title()

    def start_title(self):
        self.title_label.place(x=250, y=50, anchor="center")
        self.select_mode_label.place(x=250, y=130, anchor="center")
        self.two_player_button.place(x=250, y=210, anchor="center")
        self.algorithm_player_button.place(x=250, y=310, anchor="center")

    def remove_start_title(self):
        self.title_label.place_forget()
        self.select_mode_label.place_forget()
        self.two_player_button.place_forget()
        self.algorithm_player_button.place_forget()

    def select_first_player_title(self):
        self.choose_first_player.place(x=250, y=50, anchor="center")
        self.player_first_button.place(x=250, y=130, anchor="center")
        self.ai_first_button.place(x=250, y=230, anchor="center")
        self.random_player_button.place(x=250, y=330, anchor="center")

    def remove_select_first_player_title(self):
        self.choose_first_player.place_forget()
        self.player_first_button.place_forget()
        self.ai_first_button.place_forget()
        self.random_player_button.place_forget()

    def two_players(self):
        self.remove_start_title()
        self.player_order = (HUMAN_PLAYER, HUMAN_PLAYER)
        self.game = core.Game(self.player_order)
        self.game_screen()

    def algorithm_player(self):
        self.remove_start_title()
        self.select_first_player_title()

    def player_button(self):
        self.player_order = (HUMAN_PLAYER, AI_PLAYER)
        self.game = core.Game(self.player_order)
        self.remove_select_first_player_title()
        self.game_screen()

    def ai_button(self):
        self.player_order = (AI_PLAYER, HUMAN_PLAYER)
        self.game = core.Game(self.player_order)
        self.remove_select_first_player_title()
        self.game_screen()

    def random_button(self):
        self.player_order = [choice((-1, 1)), -1]
        if self.player_order[0] == -1:
            self.player_order[1] = 1
        self.game = core.Game(self.player_order)
        self.remove_select_first_player_title()
        self.game_screen()

    def game_screen(self):
        button = 0
        for i in range(0, 3):
            for j in range(0, 3):
                self.buttons[button].grid(row=i, column=j, padx=5, pady=5)
                button += 1
        if self.player_order[0] == AI_PLAYER:
            n_button = core.Game.turn(self.game, None)
            self.buttons[n_button].configure(text="",
                                             image=(self.x_image if self.game.symbol == CROSS else self.o_image))
            self.buttons[n_button].configure(state="disabled")

    def button_click(self, n_button):
        core.Game.turn(self.game, n_button)
        self.buttons[n_button].configure(text="", image=(self.x_image if self.game.symbol == CROSS else self.o_image))
        self.buttons[n_button].configure(state="disabled")
        self.result = core.check_winner(self.game.board)
        if self.result in [1, 0, -1]:
            self.end_title(self.result)
        elif AI_PLAYER in self.player_order:
            n_button = core.Game.turn(self.game, None)
            self.buttons[n_button].configure(text="",
                                             image=(self.x_image if self.game.symbol == CROSS else self.o_image))
            self.buttons[n_button].configure(state="disabled")
            self.result = core.check_winner(self.game.board)
            if self.result in [1, 0, -1]:
                self.end_title(self.result)

    def end_title(self, result):
        for button in self.buttons:
            button.grid_forget()
        if result == 0:
            self.end_text.configure(text="Empate")
            self.end_text.place(x=250, y=175, anchor="center")
        elif result == 1:
            self.end_text.configure(text="El jugador 1 gana")
            self.end_text.place(x=250, y=175, anchor="center")
        elif result == -1:
            self.end_text.configure(text="El jugador 2 gana")
            self.end_text.place(x=250, y=175, anchor="center")
        self.restart_button.place(x=250, y=230, anchor="center")

    def restart(self):
        self.end_text.place_forget()
        self.restart_button.place_forget()
        self.result = None
        for button in self.buttons:
            button.configure(text="", image=None, state="normal")
        self.start_title()


app = App()
app.mainloop()
