import thorpy
from settings import box_settings, get_tile_pos, backgrounds


class Gui:
    def __init__(self, screen, player, p_id, which_map):
        self.window = screen
        self.radio_buttons = []
        self.button_text = ["Move", "Basic", "Special"]
        self.gui_info_amount = len(player.heroes[0].stats)
        self.menu = None
        self.background = None
        self.elements = []
        self.radio_pool = None
        self.buttons_update_flag = 1
        self.p_id = p_id
        self.create(which_map)

    def fill_elements_table(self):
        for _ in range(self.gui_info_amount * 2):
            self.elements.append(thorpy.make_text(" ", 12, (0, 0, 0)))

    def fill_radio_buttons(self):
        for txt in self.button_text:
            rad = thorpy.Checker(txt, type_="radio")
            rad.finish()
            self.radio_buttons.append(rad)

    def create(self, which_map):
        self.fill_elements_table()
        self.fill_radio_buttons()
        self.radio_pool = thorpy.RadioPool(self.radio_buttons, first_value=self.radio_buttons[0], always_value=True)
        self.background = thorpy.Background(color=(168, 139, 50), image=backgrounds[str(which_map)],
                                            elements=self.elements + self.radio_buttons)

        self.menu = thorpy.Menu(self.background)

        for element in self.menu.get_population():
            element.surface = self.window
        thorpy.store(self.background, self.elements[:self.gui_info_amount],
                     x=10, y=125, align="center")
        thorpy.store(self.background, self.elements[self.gui_info_amount:],
                     x=box_settings["RIGHT_BOX"] + 10, y=125, align="center")
        thorpy.store(self.background, self.radio_buttons,
                     x=20 + self.p_id * box_settings["RIGHT_BOX"], y=400, align="left")

        self.buttons_appearing(0)
        self.background.blit()
        self.background.update()

    def set_hero_info(self, player, mouse_pos, opponent_info_index):
        chosen_hero = list(filter(lambda hero: hero.pos == mouse_pos, player.heroes))[0]
        for index, attribute in enumerate(chosen_hero.stats):
            value = str(chosen_hero.stats[attribute])
            self.elements[index + opponent_info_index].set_text(attribute + ": " + value)
            self.elements[index + opponent_info_index].set_visible(1)

    def get_radio_value(self):
        for index in range(len(self.radio_buttons)):
            if self.radio_buttons[index].get_value() == 1:
                return self.button_text[index].lower()

    def reset_gui(self):
        for element_id in range(len(self.elements)):
            self.elements[element_id].set_visible(0)

    def buttons_appearing(self, appear_value):
        if self.buttons_update_flag != appear_value:
            self.buttons_update_flag = appear_value
            self.radio_pool.refresh(self.radio_buttons[0])
        for rad in self.radio_buttons:
            rad.set_visible(appear_value)

    def update_gui(self, mouse_pos, player, opponent):
        self.reset_gui()
        if box_settings["BOX_WIDTH"] < mouse_pos[0] < box_settings["RIGHT_BOX"]:
            mouse_pos = get_tile_pos(mouse_pos)
            self.buttons_appearing(1) if player.clicked_hero else self.buttons_appearing(0)
            if player.clicked_own_hero(mouse_pos):
                self.set_hero_info(player, mouse_pos, self.gui_info_amount * player.player_id)
            elif player.clicked_opp_hero(opponent, mouse_pos):
                self.set_hero_info(opponent, mouse_pos, self.gui_info_amount * opponent.player_id)
        self.background.blit()
