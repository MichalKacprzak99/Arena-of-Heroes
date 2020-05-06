import pygame as pg
import thorpy
from hero import Hero
from player import Player
from settings import GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT, BOX_WIDTH, RIGHT_BOX_START, GUI_INFO, \
    get_tile_pos, coordinate


class Gui:
    def __init__(self, pygame_screen):
        self.window = pygame_screen
        self.radio_buttons = []
        self.button_text = ["Basic",  "Special", "TOBEADDED"]
        self.hero_info_text = ["Selected hero:", " ", "HP: ", " ", "Attack: ", " ", "Defense: ", " "]
        self.opponent_info_text = ["Opponent hero:"]
        self.menu = None
        self.background = None
        self.elements = []
        self.radio_pool = None
        self.create()

    def fill_elements_table(self):
        for txt in self.hero_info_text:
            self.elements.append(thorpy.make_text(" ", 12, (0, 0, 0)))
            self.elements.append(thorpy.make_text(" ", 12, (0, 0, 0)))

    def create(self):
        self.fill_elements_table()
        self.background = thorpy.Background(color=(168, 139, 50), elements=self.elements+self.radio_buttons)
        thorpy.set_theme("round")
        self.menu = thorpy.Menu(self.background)
        for element in self.menu.get_population():
            element.surface = self.window
        for txt in self.button_text:
            self.radio_buttons.append(thorpy.Checker(txt, type_="radio"))
        self.radio_pool = thorpy.RadioPool(self.radio_buttons, first_value=self.radio_buttons[0], always_value=True)

        thorpy.store(self.background, self.elements[GUI_INFO["DISPLAY_HERO"]:GUI_INFO["OPPONENT_HERO"]],
                     x=10, y=0, align="center")
        thorpy.store(self.background, self.elements[GUI_INFO["OPPONENT_HERO"]:], x=RIGHT_BOX_START + 10, y=0,
                     align="center")

        self.background.blit()
        self.background.update()

    def set_hero_info(self, player, mouse_pos):
        for hero in player.heroes:
            if hero.pos == mouse_pos:
                chosen_id = hero.hero_id
        self.elements[GUI_INFO["DISPLAY_HERO"]].set_text(self.hero_info_text[GUI_INFO["DISPLAY_HERO"]])
        self.elements[GUI_INFO["HERO_NAME"]].set_text(str(player.heroes[chosen_id].hero_id))

        self.elements[GUI_INFO["DISPLAY_HP"]].set_text(self.hero_info_text[GUI_INFO["DISPLAY_HP"]])
        self.elements[GUI_INFO["HP_VALUE"]].set_text(str(player.heroes[chosen_id].health))

        self.elements[GUI_INFO["DISPLAY_ATTACK"]].set_text(self.hero_info_text[GUI_INFO["DISPLAY_ATTACK"]])
        self.elements[GUI_INFO["ATTACK_VALUE"]].set_text("PLACEHOLDER")

        self.elements[GUI_INFO["DISPLAY_DEFENSE"]].set_text(self.hero_info_text[GUI_INFO["DISPLAY_DEFENSE"]])
        self.elements[GUI_INFO["DEFENSE_VALUE"]].set_text("PLACEHOLDER")

    def set_opponent_info(self, opponent, mouse_pos):
        for hero in opponent.heroes:
            if hero.pos == mouse_pos:
                chosen_id = hero.hero_id
        opponent_info_index = 8
        self.elements[GUI_INFO["DISPLAY_HERO"] + opponent_info_index].set_text(self.hero_info_text
                                                                               [GUI_INFO["DISPLAY_HERO"]])
        self.elements[GUI_INFO["HERO_NAME"] + opponent_info_index].set_text(str(opponent.heroes
                                                                                [chosen_id].hero_id))
        self.elements[GUI_INFO["DISPLAY_HP"] + opponent_info_index].set_text(self.hero_info_text
                                                                               [GUI_INFO["DISPLAY_HP"]])
        self.elements[GUI_INFO["HP_VALUE"] + opponent_info_index].set_text(str(opponent.heroes
                                                                               [chosen_id].health))
        self.elements[GUI_INFO["DISPLAY_ATTACK"] + opponent_info_index].set_text(self.hero_info_text
                                                                                 [GUI_INFO["DISPLAY_ATTACK"]])
        self.elements[GUI_INFO["ATTACK_VALUE"] + opponent_info_index].set_text("PLACEHOLDER")
        self.elements[GUI_INFO["DISPLAY_DEFENSE"] + opponent_info_index].set_text(self.hero_info_text
                                                                                  [GUI_INFO["DISPLAY_DEFENSE"]])
        self.elements[GUI_INFO["DEFENSE_VALUE"] + opponent_info_index].set_text("PLACEHOLDER")

    def reset_gui(self):
        for element_index in range(16):
            self.elements[element_index].set_text(" ")

    def update_gui(self, mouse_pos, player, opponent):
        if 120 < mouse_pos[0] < 888:
            mouse_pos = get_tile_pos(mouse_pos)
            if any(map(lambda hero: mouse_pos == hero.pos, player.heroes)):
                self.set_hero_info(player, mouse_pos)
            elif any(map(lambda opp_hero: mouse_pos == opp_hero.pos, opponent.heroes)):
                self.set_opponent_info(opponent, mouse_pos)
            else:
                self.reset_gui()

        self.background.blit()
