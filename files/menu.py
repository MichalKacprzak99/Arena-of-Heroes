import thorpy
from settings import COLORS
import pygame as pg

class Menu:
    def __init__(self, window):
        self.window = window
        self.menu = self.create(self)
        self.active = True
        self.start_game = False
        self.load_game = False


    @staticmethod
    def create(self):
        btn1 = thorpy.make_button("Start Game")
        btn2 = thorpy.make_button("Load Game")
        btn3 = thorpy.make_button("Quit")

        box = thorpy.Box([btn1, btn2, btn3])
        menu = thorpy.Menu(box)
        for element in menu.get_population():
            element.surface = self.window

        box.center()
        box.blit()
        box.update()
        return menu

    def click(self, mouse, network, p_id):
        for element in self.menu.get_population():
            if element.get_rect().collidepoint(mouse):
                if element.get_full_txt() == "Start Game":
                    network.send(["is_started", p_id, True])
                    return True
                elif element.get_full_txt() == "Load Game":
                    self.load_game = True
                elif element.get_full_txt() == "Quit":
                    pass
        return False


    def react(self, mouse):
        pass
