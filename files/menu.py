import thorpy
import pygame as pg
from settings import load_image

#dorobic czekanie na zaladowanie
class Menu:
    def __init__(self, window, network, p_id):
        self.p_id = p_id
        self.network = network
        self.window = window
        self.buttons = []
        self.b_text = ["Start Game", "Load Game", "Instructions", "Quit"]
        self.menu_func = {
            "Start Game": self.start_game,
            "Load Game": self.load_menu,
            "Instructions": self.instructions,
            "Quit": self.quit
        }
        self.load_buttons = []
        self.menu_box = None
        self.load_games = []
        self.menu = self.create()
        self.load_submenu = None
        self.instructions_menu = None
        self.player_ready = False
        self.opponent_ready = False
        self.active = True
        self.help = False
        self.load = False

    def create(self):
        self.background_image()

        thorpy.set_theme("round")
        self.buttons = [thorpy.make_button(txt, func=self.menu_func[txt]) for txt in self.b_text]
        [button.set_font_size(30) for button in self.buttons]
        [button.scale_to_title() for button in self.buttons]
        self.menu_box = thorpy.Box(self.buttons)
        menu = thorpy.Menu(self.menu_box)
        self.menu_box.set_main_color((0, 0, 0, 0))
        for element in menu.get_population():
            element.surface = self.window
        self.menu_box.center()
        self.menu_box.blit()
        pg.display.update()
        return menu

    def instructions(self):
        self.active = False
        self.load = False
        self.help = True
        self.draw_image("instructions.png", 50, 50)
        back = thorpy.Background(color=(0, 0, 0, 0))
        my_reaction = thorpy.Reaction(reacts_to=pg.KEYDOWN, reac_func=self.exit_instructions)
        back.add_reaction(my_reaction)
        self.instructions_menu = thorpy.Menu(back)
        pg.display.update()

    def load_menu(self):
        self.active = False
        self.load = True
        self.help = False
        self.background_image()
        self.load_games = self.network.send(["get_games_to_load"])
        self.load_buttons = [thorpy.make_button(str(game), func=self.load_game, params={"which_game": i})
                             for i, game in enumerate(self.load_games)]
        quit_button = thorpy.make_button("Quit", func=self.quit_submenu)
        self.load_buttons.append(quit_button)
        [button.set_font_size(20) for button in self.load_buttons]
        [button.scale_to_title() for button in self.load_buttons]
        box = thorpy.Box(self.load_buttons)
        self.load_submenu = thorpy.Menu(box)
        box.set_main_color((0, 0, 0, 0))
        for element in self.load_submenu.get_population():
            element.surface = self.window
        box.center()
        box.blit()
        pg.display.update()

    def load_game(self, which_game):
        self.network.send(["load", self.load_games[which_game]])
        self.start_game()

    def exit_instructions(self, event):
        if event.key == pg.K_SPACE:
            self.help = False
            self.active = True
            self.background_image()
            self.menu_box.blit()
            pg.display.update()

    def start_game(self):
        self.network.send(["is_ready", self.p_id, True])
        self.player_ready = True
        self.active = False

    def both_ready(self):
        return self.player_ready and self.opponent_ready

    def waiting_for_opp(self):
        return self.player_ready is True and self.opponent_ready is False

    def background_image(self):
        image = pg.image.load(load_image("menu_background.jpg"))
        rect = image.get_rect()
        rect.left, rect.top = 0, 0
        self.window.blit(image, rect)

    @staticmethod
    def quit():
        pg.quit()

    def loading_screen(self):
        self.background_image()
        self.draw_text("Game will start soon", 300, 200, 23)
        pg.display.update()

    def draw_text(self, text_to_input, pos_x, pos_y, size=15):
        font = pg.font.SysFont("Arial", size)
        text = font.render(text_to_input, True, (0, 0, 0))
        self.window.blit(text, (pos_x, pos_y))

    def draw_image(self, image_path, pos_x, pos_y):
        image = pg.image.load(load_image(image_path))
        rect = image.get_rect()
        rect.left, rect.top = pos_x, pos_y
        self.window.blit(image, rect)

    def quit_submenu(self):
        self.active = True
        self.load = False
        self.background_image()
        self.menu_box.blit()
        pg.display.update()

    def highlight_buttons(self, event):
        if self.active is True:
            self.menu.react(event)
        elif self.load is True:
            self.load_submenu.react(event)
        elif self.help is True:
            self.instructions_menu.react(event)
