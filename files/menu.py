import thorpy
import pygame as pg
from settings import load_image


class Menu:
    def __init__(self, window):
        self.window = window
        self.buttons = []
        self.b_text = ["Start Game", "Load Game", "Instructions", "Quit"]
        self.menu = self.create()
        self.player_ready = False
        self.opponent_ready = False

    def create(self):
        self.background_image()

        thorpy.set_theme("round")
        self.buttons = [thorpy.make_button(txt) for txt in self.b_text]
        box = thorpy.Box(self.buttons)
        menu = thorpy.Menu(box)
        for element in menu.get_population():
            element.surface = self.window

        box.center()
        box.blit()
        pg.display.update()
        return menu

    def click(self, mouse, network, p_id):
        for element in self.menu.get_population():
            if element.get_rect().collidepoint(mouse) and self.player_ready is False:
                if element.get_full_txt() == "Start Game":
                    network.send(["is_ready", p_id, True])
                    self.player_ready = True
                elif element.get_full_txt() == "Load Game":
                    pass
                elif element.get_full_txt() == "Instructions":
                    pass
                elif element.get_full_txt() == "Quit":
                    pass

    def both_ready(self):
        return self.player_ready and self.opponent_ready

    def waiting_for_opp(self):
        return self.player_ready is True and self.opponent_ready is False

    def background_image(self):
        image = pg.image.load(load_image("background.jpg"))
        rect = image.get_rect()
        rect.left, rect.top = 0, 0
        self.window.blit(image, rect)

    def loading_screen(self):
        self.background_image()
        font = pg.font.SysFont("Arial", 23)
        text_to_input = "Game will start soon"
        text = font.render(text_to_input, True, (0, 0, 0))
        self.window.blit(text, (300, 200))
        pg.display.update()
