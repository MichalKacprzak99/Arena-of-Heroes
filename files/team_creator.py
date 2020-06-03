import thorpy
import pygame as pg
from settings import load_image, icons
from hero import Healer, Mage, Warrior, Archer
from os import path


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
            "Archer": Archer,
        }
        self.heroes = [thorpy.make_button(txt, func=self.change_hero, params={"name": txt})
                       for txt in self.classes.keys()]
        self.box = thorpy.Box(self.heroes)
        self.menu = thorpy.Menu(self.box)
        self.chosen = "Healer"
        self.team = [None, None, None, None]
        self.count = 0
        self.options = {
            "Back": self.back_to_menu,
            "Ready": self.start_game
        }

        self.options_dos = {
            "Add": self.add_hero,
            "Delete": self.delete_hero
        }

        self.opt_buttons = [thorpy.make_button(txt, func=self.options[txt]) for txt in self.options.keys()]
        self.box_down = thorpy.Box(self.opt_buttons)
        self.menu_down = thorpy.Menu(self.box_down)

        self.opt_two = [thorpy.make_button(txt, func=self.options_dos[txt]) for txt in self.options_dos.keys()]
        self.box_mid = thorpy.Box(self.opt_two)
        self.menu_mid = thorpy.Menu(self.box_mid)
        self.lore={
            "Healer": ["Healer is very valuable hero to have on your team.",
                       "His healing may turn the tables around in battle.",
                       "But at the cost of not being able to do much damage..."],
            "Mage": ["Mage can be described with one word: unpredictable",
                     "His skill can do very little or very much damage ",
                     "and also damages one random enemy"],
            "Warrior": ["Arrrgh", "Warrior is a simple hero to play with.",
                        "Position yourself well, then do much damage to opponent."],
            "Archer": ["Archer was peaceful and calm person training his skills for good cause ... ",
                       "... but when one day his pet duck Carlos was kidnapped, he changed drastically!",
                       "Now his goal is to kill everyone who stands in his way of reuniting with his buddy",
                       " ", "This hero centers around quick movement and sneaky attacks.",
                       "It's special attack hits harder when enemy is far away from you",
                       "Make sure to position this hero well on board to take advantage of this skill effect"]
        }
        self.remove = [None, None, None, None]
        self.prepare_menu()

    def start_game(self):
        team = self.make_team(self.p_id)
        self.network.send(["is_ready", self.p_id, True, team])
        self.parent_menu.player_ready = True
        self.parent_menu.control["creator"][0] = False

    def prepare_menu(self):
        self.prepare_menu_buttons(self.heroes, self.box, self.menu, 160, 10, 20)
        self.prepare_menu_buttons(self.opt_two, self.box_mid, self.menu_mid, 460, 580, 60)
        self.prepare_menu_buttons(self.opt_buttons, self.box_down, self.menu_down, 160, 660, 300)
        
        self.opt_two[1].active = False
        self.opt_buttons[1].active = False

    def prepare_menu_buttons(self, buttons, box,  menu, x, y, g):
        [button.set_font_size(30) for button in buttons]
        [button.scale_to_title() for button in buttons]
        box.set_main_color((0, 0, 0, 0))
        thorpy.store(box, mode="h",  gap=g)
        box.fit_children()
        box.set_topleft((x, y))
        for element in menu.get_population():
            element.surface = self.window

    def creator_view(self):
        self.draw_image('picker_background.jpg', 0, 0)
        self.box.blit()
        self.box_down.blit()
        self.box_mid.blit()
        self.draw_outlines()
        self.display_hero()

        pos = iter((140 + i*100) for i in range(len(self.team)))
        [self.show_hero(hero, 620, next(pos)) for hero in self.team]
        pg.display.update()

    def react(self, event):
        self.menu.react(event)
        self.menu_down.react(event)
        self.menu_mid.react(event)

    def add_hero(self):
        if self.count < 4:
            self.team[self.count] = self.chosen
            self.count += 1
        if self.count == 4:
            self.opt_buttons[1].active = True
        if self.count > 0:
            self.opt_two[1].active = True

    def show_hero(self, name, x=100, y=100, mode=2):
        if name is not None:
            name = name.upper()
            path = name
            if mode is 2:
                path +="\south.png"
            else:
                path += "\portrait.png"
            self.draw_image(path, x, y, mode)

    def draw_text(self, text_to_input, pos_x, pos_y, size=15):
        font = pg.font.SysFont("Arial", size)
        text = font.render(text_to_input, True, (0, 0, 0))
        self.window.blit(text, (pos_x, pos_y))

    def draw_image(self, image_path, pos_x, pos_y, mode=0):
        image = pg.image.load(load_image(image_path))
        if mode is 1:
            image = pg.transform.scale(image, (200, 200))
        rect = image.get_rect()
        rect.left, rect.top = pos_x, pos_y
        self.window.blit(image, rect)

    def load_icon(self, filename):
        game_folder = path.dirname(__file__)
        image_folder = path.join(game_folder)
        return path.join(image_folder, str(filename))

    def make_team(self, p_id):
        pos = iter([[11*p_id, i] for i in range(1, 11, 3)])
        side = "west" if p_id == 1 else "east"
        table = []
        for i in range(4):
            table.append(self.make_hero(i, self.team[i], next(pos), side))
        return table

    def make_hero(self, id, name, pos, side):
        return self.classes[name](id, pos, side)

    def change_hero(self, name):
        self.chosen = name

    def delete_hero(self):
        self.team[self.count-1] = None
        self.count -= 1
        if self.count <= 0:
            self.opt_two[1].active = False
        if self.count < 4:
            self.opt_buttons[1].active = False
    
    def back_to_menu(self):
        self.active = False
        self.parent_menu.player_ready = False
        self.parent_menu.control["creator"][0] = False
        self.parent_menu.quit_submenu()

    def draw_icons(self, stats):
        pos = iter((150 + i*25) for i in range(len(stats)))
        for item in icons.keys():
            image = pg.image.load(self.load_icon(icons[item]))
            rect = image.get_rect()
            rect.left, rect.top = 300, next(pos)
            self.window.blit(image, rect)

    def show_stats(self):
        self.draw_text("Stats", 300, 100, 24)
        stats = self.classes[self.chosen](-1, -1, -1).stats
        self.draw_icons(stats)
        pos = iter((130 + i*25) for i in range(len(stats)))
        for item in stats.keys():
            self.draw_text(str(stats[item]), 330, next(pos))

    def draw_outlines(self):
        color = (139, 69, 19)
        pos = {(0, 75, 800, 75), (0, 645, 800, 645), (540, 75, 540, 645),
               (0, 345, 540, 345), (270, 75, 270, 345)}
        for (a, b, c, d) in pos:
            pg.draw.line(self.window, color, (a, b), (c, d))

    def display_hero(self):
        self.show_hero(self.chosen, 40, 150, 1)
        self.draw_text(self.chosen, 85, 110, 30)
        self.show_stats()
        pos = iter((360 + i*24) for i in range(len(self.lore[self.chosen])))
        for line in self.lore[self.chosen]:
            self.draw_text(line, 10, next(pos))
