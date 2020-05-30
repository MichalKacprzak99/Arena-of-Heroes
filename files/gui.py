import thorpy
from settings import box_sets, get_tile_pos, backgrounds, icons, game_sets
import pygame as pg


class Gui:
    def __init__(self, screen, player, which_map, network):
        self.player = player
        self.window = screen
        self.radio_buttons = []
        self.radio_butt_text = ["Move", "Basic", "Special"]
        self.gui_info_amount = len(player.heroes[0].stats)
        self.network = network
        self.menu = None
        self.background = None
        self.elements = []
        self.radio_pool = None
        self.icons = []
        self.icons_move_flag = 0
        self.buttons_update_flag = 1
        self.create(which_map)

    def fill_elements_table(self):
        for _ in range(self.gui_info_amount * 2):
            if _ == 0 or _ == self.gui_info_amount:
                self.elements.append(thorpy.make_text(" ", 23, (0, 0, 0)))
            else:
                self.elements.append(thorpy.make_text(" ", 19, (0, 0, 0)))

    def fill_radio_buttons(self):
        for txt in self.radio_butt_text:
            rad = thorpy.Checker(txt, type_="radio")
            rad.finish()
            self.radio_buttons.append(rad)

    def make_buttons(self):
        save_button = thorpy.make_button("Save", func=self.network.send, params={"data": ["save"]})
        quit_button = thorpy.make_button("Quit", func=pg.quit)
        buttons = [save_button, quit_button]
        [button.set_font_size(20) for button in buttons]
        [button.scale_to_title() for button in buttons]
        return buttons

    def create(self, which_map):
        self.fill_elements_table()
        self.fill_radio_buttons()
        self.fill_icons_table()
        buttons = self.make_buttons()
        self.radio_pool = thorpy.RadioPool(self.radio_buttons, first_value=self.radio_buttons[0], always_value=True)
        self.background = thorpy.Background(color=(168, 139, 50), image=backgrounds[str(which_map)],
                                            elements=self.elements + self.radio_buttons+buttons + self.icons)
        self.menu = thorpy.Menu(self.background)
        for element in self.menu.get_population():
            element.surface = self.window
        self.place_elements(buttons)
        self.buttons_appearing(0)
        self.background.blit()
        self.background.update()

    def place_elements(self, buttons):
        thorpy.store(self.background, buttons, x=50 + self.player.p_id * box_sets["RIGHT_BOX"], y=500, align="center")
        thorpy.store(self.background, self.icons, x=17, y=145, align="center")
        thorpy.store(self.background, [self.elements[0]],
                     x=10, y=115, align="center")
        thorpy.store(self.background, self.elements[1:self.gui_info_amount],
                     x=37, y=145, align="center")
        thorpy.store(self.background, [self.elements[self.gui_info_amount]],
                     x=box_sets["RIGHT_BOX"] + 10, y=115, align="center")
        thorpy.store(self.background, self.elements[self.gui_info_amount + 1:],
                     x=box_sets["RIGHT_BOX"] + 37, y=145, align="center")
        thorpy.store(self.background, self.radio_buttons,
                     x=20 + self.player.p_id * box_sets["RIGHT_BOX"], y=400, align="left")

    def fill_icons_table(self):
        for icon in icons.values():
            image_to_add = thorpy.Image(path=icon, finish=True)
            image_to_add.finish()
            self.icons.append(image_to_add)

    def set_hero_info(self, player, mouse_pos, opponent_info_index):
        if opponent_info_index != self.icons_move_flag * self.gui_info_amount:
            self.icons_move_flag = opponent_info_index % (self.gui_info_amount - 1)
            if self.icons_move_flag == 0:
                [icon.move((-game_sets["GAME_SCREEN_WIDTH"] - box_sets["BOX_WIDTH"], 0)) for icon in self.icons]
            if self.icons_move_flag == 1:
                [icon.move((game_sets["GAME_SCREEN_WIDTH"] + box_sets["BOX_WIDTH"], 0)) for icon in self.icons]
        chosen_hero = list(filter(lambda hero: hero.pos == mouse_pos, player.heroes))[0]
        for index, attribute in enumerate(chosen_hero.stats):
            value = str(chosen_hero.stats[attribute])
            self.elements[index + opponent_info_index].set_text(value)
            self.elements[index + opponent_info_index].set_visible(1)
        [icon.set_visible(1) for icon in self.icons]

    def get_radio_value(self):
        for button in self.radio_buttons:
            if button.get_value() == 1:
                return button.get_text().lower()

    def reset_gui(self):
        for element_id in range(len(self.elements)):
            self.elements[element_id].set_visible(0)
        [icon.set_visible(0) for icon in self.icons]

    def buttons_appearing(self, appear_value):
        if self.buttons_update_flag != appear_value:
            self.buttons_update_flag = appear_value
            self.radio_pool.refresh(self.radio_buttons[0])
        [rad.set_visible(appear_value) for rad in self.radio_buttons]

    def update_gui(self, mouse_pos, player, opponent):
        self.reset_gui()
        if box_sets["BOX_WIDTH"] < mouse_pos[0] < box_sets["RIGHT_BOX"]:
            mouse_pos = get_tile_pos(mouse_pos)
            self.buttons_appearing(1) if player.clicked_hero else self.buttons_appearing(0)
            if player.clicked_own_hero(mouse_pos):
                self.set_hero_info(player, mouse_pos, self.gui_info_amount * player.p_id)
            elif player.clicked_opp_hero(opponent, mouse_pos):
                self.set_hero_info(opponent, mouse_pos, self.gui_info_amount * opponent.p_id)
        self.background.blit()

    def click(self, event):
        self.menu.react(event)
