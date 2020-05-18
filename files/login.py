from menu import Menu
import thorpy
import pygame as pg
from settings import game_settings, colors
from network import Network


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
        self.cover_boxes = []
        self.inserter_move_flag = False
        self.inserters = ["login", 0, "password", 0]
        self.state = []
        self.background = None
        self.player_logged_in = False
        self.draw_window = {
            "main_menu": self.main_menu,
            "login": self.login_menu,
            "sign up": self.sign_up_menu
        }
        self.menu = self.create()

    def login_button_function(self):
        self.state.append("login")

    def sign_up_button_function(self):
        self.state.append("sign up")

    def go_back(self):
        self.state.pop()

    def send_info(self):
        login_box = self.inserters[1]
        password_box = self.inserters[3]
        login = login_box._inserted
        password = password_box._inserted
        print(login)
        print(password)
        reply = None
        current_login_window = self.state[-1]
        if len(login) > 15 or len(password) > 15:
            self.texts[1].set_text("It seems your login or password are too long. Please don't input more than 15 "
                                   "characters.")
        elif len(login) == 0 or len(password) == 0:
            self.texts[1].set_text("It seems you didn't provide any input. Please try again.")
        else:
            print(current_login_window)
            reply = self.network.send([current_login_window, login, password])
            if reply:
                if current_login_window == "login":
                    self.texts[1].set_text("Congratulations! You managed to log in!")
                    pg.time.delay(500)
                    self.player_logged_in = True
                elif current_login_window == "sign up":
                    self.texts[1].set_text("Congratulations! You managed to create an account!")
            elif reply is False:
                if current_login_window == "login":
                    self.texts[1].set_text("Your login and/or password are incorrect. Try again.")
                elif current_login_window == "sign up":
                    self.texts[1].set_text("There exists an account with this username")
            else:
                if current_login_window == "login":
                    self.texts[1].set_text("Something wrong happened when trying to log in. Try again.")
                elif current_login_window == "sign up":
                    self.texts[1].set_text("Something wrong happened when trying to create your account. Try again.")

    def main_menu(self):
        self.reset_inserter_value()
        self.hide_buttons()
        self.hide_inserters()
        self.buttons[0].set_visible(1)
        self.buttons[1].set_visible(1)
        self.buttons[0].set_active(1)
        self.buttons[1].set_active(1)

        self.background.blit()
        self.background.update()

    def login_menu(self):
        self.hide_buttons()
        self.buttons[2].set_visible(1)
        self.buttons[3].set_visible(1)
        self.buttons[2].set_active(1)
        self.buttons[3].set_active(1)
        self.texts[0].set_text("Login")
        self.show_inserters()

        self.background.blit()
        self.background.update()

    def sign_up_menu(self):
        self.hide_buttons()
        self.buttons[2].set_visible(1)
        self.buttons[3].set_visible(1)
        self.buttons[2].set_active(1)
        self.buttons[3].set_active(1)
        self.texts[0].set_text("Create a new account!")
        self.show_inserters()

        self.background.blit()
        self.background.update()

    def hide_buttons(self):
        for button in self.buttons:
            button.set_visible(0)
            button.set_active(0)

    def hide_inserters(self):
        for inserter in self.inserters:
            inserter.set_visible(0)
        for cover_box in self.cover_boxes:
            cover_box.set_visible(1)

    def reset_inserter_value(self):
        for inserter in self.inserters:
            inserter._value = ""
            inserter._inserted = ""

    def show_inserters(self):
        for inserter in self.inserters:
            inserter.set_visible(1)
        for cover_box in self.cover_boxes:
            cover_box.set_visible(0)

    def create(self):
        self.state.append("main_menu")
        for text, button_function in self.b_info.items():
            self.buttons.append(thorpy.make_button(text, button_function))
        for text in self.text_info:
            self.texts.append(thorpy.make_text(text))
        for index in range(0, len(self.inserters), 2):
            text_to_add = self.inserters[index]
            self.inserters[index] = thorpy.make_text(text_to_add)
            self.inserters[index+1] = (thorpy.Inserter(value="", size=(200, 20), quit_on_click=False, finish=True))
            self.cover_boxes    .append(thorpy.Image(path = None, color = (168, 139, 50)))
        self.background = thorpy.Background(color=(168, 139, 50), image=None,
                                            elements=self.buttons+self.texts+self.inserters+self.cover_boxes)
        thorpy.store(self.background, self.buttons[0:2], x=game_settings["GAME_SCREEN_WIDTH"]/2,
                     y=game_settings["GAME_SCREEN_HEIGHT"]/2 - 150, align="center")
        thorpy.store(self.background, self.buttons[2:4], x=game_settings["GAME_SCREEN_WIDTH"]/2,
                     y=game_settings["GAME_SCREEN_HEIGHT"]/2, align="center")
        thorpy.store(self.background, self.inserters, x=game_settings["GAME_SCREEN_WIDTH"]/2,
                     y=game_settings["GAME_SCREEN_HEIGHT"]/2 - 100, align="center")
        thorpy.store(self.background, [self.texts[0]], x=game_settings["GAME_SCREEN_WIDTH"] / 2,
                     y=game_settings["GAME_SCREEN_HEIGHT"] / 2 - 200, align="center")
        thorpy.store(self.background, [self.texts[1]], x=game_settings["GAME_SCREEN_WIDTH"] / 2 - 200,
                     y=game_settings["GAME_SCREEN_HEIGHT"] / 2 + 100, align="left")
        thorpy.store(self.background, self.cover_boxes, x=game_settings["GAME_SCREEN_WIDTH"] / 2 - 60,
                     y=game_settings["GAME_SCREEN_HEIGHT"] / 2 - 77, align="center")
        self.menu = thorpy.Menu(self.background)
        for element in self.menu.get_population():
            element.surface = self.window
        self.background.blit()
        self.background.update()
        return self.menu

    def run(self, clock):
        while not self.player_logged_in:
            clock.tick(60)
            current_login_window = self.state[-1]
            self.draw_window[current_login_window]()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                self.menu.react(event)






