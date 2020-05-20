import thorpy
import pygame as pg
from settings import load_image
from hero import Healer, Mage, Warrior, Archer


class TeamCreator:
    def __init__(self, window, network, p_id, parent_menu):
        self.window = window
        self.network = network
        self.p_id = p_id
        self.parent_menu = parent_menu
        self.active = False
        self.classes = {
            "Healer": Healer,
            "Mage": Mage,
            "Warrior": Warrior,
            "Archer": Archer
        }
        self.buttons = [thorpy.make_button(txt, func=self.show_hero, params={"name": txt})
                        for txt in self.classes.keys()]
        self.box = thorpy.Box(self.buttons)
        self.menu = thorpy.Menu(self.box)
        self.chosen = "Healer"
        self.team = []
        self.add = thorpy.make_button("ADD TO TEAM", func=self.add_hero)
        self.ready_button = thorpy.make_button("READY", func=self.start_game)
        self.prepare_menu()

    def start_game(self):
        team = self.make_team(self.p_id)
        self.network.send(["is_ready", self.p_id, True, team])
        self.parent_menu.player_ready = True
        self.active = False

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

    def picker_view(self):
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

    def react(self, event):
        if self.menu is not None:
            self.menu.react(event)
            self.add.react(event)
            self.ready_button.react(event)

    def add_hero(self):
        if len(self.team) < 4:
            self.team.append(self.chosen)
        if len(self.team) == 4:
            self.ready_button.active = True

    def show_hero(self, name, x=100, y=100):
        self.chosen = name
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

    def make_team(self, p_id):
        pos = iter([[11*p_id, i] for i in range(1, 11, 3)])
        side = "west" if p_id == 1 else "east"
        table = []
        for i in range(4):
            table.append(self.make_hero(i, self.team[i], next(pos), side))
        return table

    def make_hero(self, id, name, pos, side):
        return self.classes[name](id, pos, side)
