import thorpy
import pygame as pg
from settings import game_sets, colors


class LoginScreen:
    def __init__(self, window, network):
        self.network = network
        self.window = window
        self.buttons = []
        self.b_info = {
            "Login": self.login_button_function,
            "Sign up": self.sign_up_button_function,
            "Return": self.go_back,
            "Enter": self.send_info
        }
        self.text_info = ["Welcome to Arena of Heroes!", " "]
        self.texts = []
        self.inserter_text = ["login", "password"]
        self.inserters = []
        self.state = []
        self.background = None
        self.player_logged_in = False
        self.draw_window = {
            "main_menu": self.main_menu,
            "login": self.login_menu,
            "sign up": self.sign_up_menu
        }
        self.menu = self.create()

    def update_background(self):
        self.background.blit()
        self.background.update()

    def login_button_function(self):
        self.state.append("login")

    def sign_up_button_function(self):
        self.state.append("sign up")

    def go_back(self):
        self.state.pop()

    def send_info(self):
        login_box = self.inserters[1]
        password_box = self.inserters[3]
        login = login_box.get_value()
        password = password_box.get_value()
        current_login_window = self.state[-1]
        if len(login) > 15 or len(password) > 15:
            self.texts[1].set_text("It seems your login or password are too long.")
            self.texts[2].set_text("Please don't input more than 15 characters.")
        elif len(login) == 0 or len(password) == 0:
            self.texts[1].set_text("It seems you didn't provide any input. Please try again.")
            self.texts[2].set_text("")
        else:
            reply = self.network.send([current_login_window, login, password])
            if reply:
                if current_login_window == "login":
                    self.texts[1].set_text("Congratulations! You managed to log in!")
                    self.texts[2].set_text("")
                    self.update_background()
                    pg.time.delay(500)
                    self.player_logged_in = True
                elif current_login_window == "sign up":
                    self.texts[1].set_text("Congratulations!")
                    self.texts[2].set_text("You managed to create an account!")
            elif reply is False:
                if current_login_window == "login":
                    self.texts[1].set_text("Your data is incorrect or somebody")
                    self.texts[2].set_text("is logged in on this account. Try again.")
                elif current_login_window == "sign up":
                    self.texts[1].set_text("There exists an account with this username")
                    self.texts[2].set_text("")
            else:
                if current_login_window == "login":
                    self.texts[1].set_text("Something wrong happened when trying to log in. Try again.")
                    self.texts[2].set_text("")
                elif current_login_window == "sign up":
                    self.texts[1].set_text("Something wrong happened when trying to create your account. Try again.")
                    self.texts[2].set_text("")

    def main_menu(self):
        self.reset_inserter_value()
        self.hide_inserters()
        login_button_index = 0
        sign_up_button_index = 1
        self.enable_buttons(login_button_index, sign_up_button_index)
        self.texts[0].set_text("Welcome to Arena Of Heroes!")
        self.texts[1].set_text("")
        self.texts[2].set_text("")
        self.update_background()

    def create_login_signup_menu(self):
        return_button_index = 2
        enter_button_index = 3
        self.enable_buttons(return_button_index, enter_button_index)
        self.show_inserters()

    def login_menu(self):
        self.create_login_signup_menu()
        self.texts[0].set_text("Login")
        self.update_background()

    def sign_up_menu(self):
        self.create_login_signup_menu()
        self.texts[0].set_text("Create a new account!")
        self.update_background()

    def enable_buttons(self, index_start, index_end):
        for index in range(len(self.buttons)):
            if index_start <= index <= index_end:
                self.buttons[index].set_visible(1)
                self.buttons[index].set_active(1)
            else:
                self.buttons[index].set_visible(0)
                self.buttons[index].set_active(0)

    def hide_buttons(self):
        for button in self.buttons:
            button.set_visible(0)
            button.set_active(0)

    def hide_inserters(self):
        [inserter.set_visible(0) for inserter in self.inserters]

    def reset_inserter_value(self):
        for index in range(0, len(self.inserters), 2):
            self.inserters[index+1].set_value("", refresh_draw=True)

    def show_inserters(self):
        [inserter.set_visible(1) for inserter in self.inserters]

    def fill_buttons_list(self):
        thorpy.set_theme("round")
        for text, button_function in self.b_info.items():
            button_to_add = thorpy.make_button(text, button_function)
            button_to_add.set_font_size(20)
            button_to_add.scale_to_title()
            self.buttons.append(button_to_add)

    def fill_text_list(self):
        text_to_add = thorpy.make_text(self.text_info[0])
        text_to_add.set_font_size(20)
        text_to_add.set_font_color(colors["BUMBLEBEE"])
        self.texts.append(text_to_add)
        for text in self.text_info:
            info_text = thorpy.make_text("")
            info_text.set_font_size(20)
            info_text.set_font_color(colors["RED"])
            self.texts.append(info_text)

    def fill_inserters(self):
        for text in self.inserter_text:
            text_to_add = thorpy.make_text(text)
            text_to_add.set_font_size(20)
            text_to_add.set_font_color(colors["BUMBLEBEE"])
            self.inserters.append(text_to_add)
            self.inserters.append(thorpy.Inserter(value="", size=(300, 30), quit_on_click=False, finish=True))

    def place_elements_on_background(self):
        thorpy.store(self.background, self.buttons[0:2], x=game_sets["GAME_SCREEN_WIDTH"] / 2,
                     y=game_sets["GAME_SCREEN_HEIGHT"] / 2 - 100, align="center")
        thorpy.store(self.background, self.buttons[2:4], x=game_sets["GAME_SCREEN_WIDTH"] / 2,
                     y=game_sets["GAME_SCREEN_HEIGHT"] / 2 + 100, align="center")
        thorpy.store(self.background, self.inserters, x=game_sets["GAME_SCREEN_WIDTH"] / 2,
                     y=game_sets["GAME_SCREEN_HEIGHT"] / 2 - 100, align="center")
        thorpy.store(self.background, [self.texts[0]], x=game_sets["GAME_SCREEN_WIDTH"] / 2,
                     y=game_sets["GAME_SCREEN_HEIGHT"] / 2 - 200, align="center")
        thorpy.store(self.background, self.texts[1:3], x=game_sets["GAME_SCREEN_WIDTH"] / 2 - 225,
                     y=game_sets["GAME_SCREEN_HEIGHT"] / 2 + 200, align="left")

    def create(self):
        self.state.append("main_menu")
        self.fill_buttons_list()
        self.fill_text_list()
        self.fill_inserters()
        self.background = thorpy.Background(color=None, image="backgrounds/login_background.png",
                                            elements=self.buttons+self.texts+self.inserters)
        self.place_elements_on_background()
        self.menu = thorpy.Menu(self.background)
        for element in self.menu.get_population():
            element.surface = self.window
        self.update_background()
        return self.menu

    def run(self, clock):
        while not self.player_logged_in:
            clock.tick(60)
            current_login_window = self.state[-1]
            try:
                self.draw_window[current_login_window]()
            except pg.error:
                break
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                self.menu.react(event)
