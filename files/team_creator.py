import thorpy
import pygame as pg
from settings import load_image


class TeamCreator:
    def __init__(self, window):
        self.window = window
        self.classes_text = ["Healer", "Mage", "Warrior", "Archer"]
        self.buttons = [thorpy.make_button(txt) for txt in self.classes_text]
        self.box = thorpy.Box(self.buttons)
        self.menu = thorpy.Menu(self.box)
        self.chosen = "Healer"
        self.team = []
        self.add = thorpy.make_button("ADD TO TEAM")
        self.ready_button = thorpy.make_button("READY")
        self.start = False
        self.prepare_menu()

    def prepare_menu(self):
        self.box.set_main_color((0, 0, 0))
        self.box.center(-200, 160)
        for element in self.menu.get_population():
            element.surface = self.window
        self.add.surface = self.window
        self.add.center(-200, -120)
        self.ready_button.active = False
        self.ready_button.surface = self.window
        self.ready_button.set_main_color((230, 255, 0, 100))
        self.ready_button.center(200, 200)

    def creator_background(self):
        self.draw_image('picker_background.png', 0, 0)
        self.box.blit()
        self.add.blit()
        self.ready_button.blit()
        self.draw_text(self.chosen, 125, 60, 70)
        self.show_hero(self.chosen, 130, 170)
        x = 400
        for hero in self.team:
            self.show_hero(hero, x, 460)
            x+=64
        self.draw_text("Choose class", 100, 400, 30)
        self.draw_text("Your team", 500, 400, 30)
        pg.display.update()

    def highlight_on_hover(self, event):
        if self.menu is not None:
            self.menu.react(event)
            self.add.react(event)
            self.ready_button.react(event)

    def react_to_click(self, mouse, network, p_id):
        if self.menu is not None:
            for element in self.menu.get_population():
                if element.get_rect().collidepoint(mouse) and isinstance(element, thorpy.elements.clickable.Clickable):
                    self.chosen = element.get_full_txt()
            if self.add.get_rect().collidepoint(mouse):
                self.add_hero(self.chosen)
                if len(self.team) == 4:
                    self.ready_button.active = True
                    self.ready_button.set_main_color((230, 0, 0))
            elif self.ready_button.get_rect().collidepoint(mouse):
                if len(self.team) == 4:
                    self.start = True
                    network.send(["is_ready", p_id, True])

    def add_hero(self, name):
        if len(self.team) < 4:
            self.team.append(name)

    def show_hero(self, name, x=100, y=100):
        name = name.upper()
        path = name + "\south.png"
        self.draw_image(path, x, y)

    def draw_text(self, text_to_input, pos_x, pos_y, size=15):
        font = pg.font.SysFont("Arial", size)
        text = font.render(text_to_input, True, (0, 0, 0))
        self.window.blit(text, (pos_x, pos_y))

    def draw_image(self, image_path, pos_x, pos_y):
        image = pg.image.load(load_image(image_path))
        rect = image.get_rect()
        rect.left, rect.top = pos_x, pos_y
        self.window.blit(image, rect)