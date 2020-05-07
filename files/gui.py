import thorpy
from settings import BOX_SETTINGS, GUI_INFO, get_tile_pos


class Gui:
    def __init__(self, pygame_screen):
        self.window = pygame_screen
        self.radio_buttons = []
        self.button_text = ["Basic",  "Special", "TOBEADDED"]
        self.hero_info_text = ["Hero:", " ", "HP: ", " ", "Attack: ", " ", "Defense: ", " "]
        self.menu = None
        self.background = None
        self.elements = []
        self.radio_pool = None
        self.create()

    def fill_elements_table(self):
        for _ in self.hero_info_text:
            self.elements.append(thorpy.make_text(" ", 12, (0, 0, 0)))

    def create(self):
        self.fill_elements_table()
        for txt in self.button_text:
            rad = thorpy.Checker(txt, type_="radio")
            rad.finish()
            self.radio_buttons.append(rad)
        self.radio_pool = thorpy.RadioPool(self.radio_buttons, first_value=self.radio_buttons[0], always_value=True)
        self.background = thorpy.Background(color=(168, 139, 50), elements=self.elements+self.radio_buttons)
        thorpy.set_theme("round")
        self.menu = thorpy.Menu(self.background)
        for element in self.menu.get_population():
            element.surface = self.window
        thorpy.store(self.background, self.elements[GUI_INFO["HERO_NAME"]:GUI_INFO["OPPONENT_HERO"]],
                     x=10, y=100, align="center")
        thorpy.store(self.background, self.elements[GUI_INFO["OPPONENT_HERO"]:],
                     x=BOX_SETTINGS["RIGHT_BOX"] + 10, y=100, align="center")
        thorpy.store(self.background, self.radio_buttons, x=20, y= 400, align="left")
        self.background.blit()
        self.background.update()

    def set_hero_info(self, player, mouse_pos, opponent_info_index):
        chosen_hero = list(filter(lambda hero: hero.pos == mouse_pos, player.heroes))[0]
        self.hero_info_text[1] = str(chosen_hero.hero_id)
        self.hero_info_text[3] = str(chosen_hero.health)
        self.hero_info_text[5] = "0"
        self.hero_info_text[7] = "0"
        for index in range (4):
            display_index = 2*index+1
            self.elements[index + opponent_info_index].set_text(self.hero_info_text[2*index] +
                                                                self.hero_info_text[display_index])

    def reset_gui(self):
        for element_id in range(len(self.elements)):
            self.elements[element_id].set_text(" ")

    def update_gui(self, mouse_pos, player, opponent):
        if 120 < mouse_pos[0] < 888:
            mouse_pos = get_tile_pos(mouse_pos)
            if player.clicked_own_hero(mouse_pos):
                self.set_hero_info(player, mouse_pos, 0 if player.player_id == 0 else 4)
            elif player.clicked_opponent_hero(opponent, mouse_pos):
                self.set_hero_info(opponent, mouse_pos, 4 if player.player_id == 0 else 0)
            else:
                self.reset_gui()

        self.background.blit()
