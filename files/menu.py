import thorpy
import pygame as pg
from settings import load_image
from team_creator import TeamCreator


class Menu:
    def __init__(self, window, network, p_id):
        self.p_id = p_id
        self.network = network
        self.window = window
        self.menu_func = {
            "Start Game": self.almost_start_game,
            "Load Game": self.load_menu,
            "Instructions": self.load_instructions,
            "Quit": self.quit
        }
        self.was_loaded = False
        self.load_box = None
        self.menu_box = None
        self.load_submenu = self.create_load_menu()
        self.menu = self.create_menu()
        self.instructions_menu = self.create_instructions()
        self.player_ready = False
        self.opponent_ready = False
        self.tc = TeamCreator(self.window, self.network, self.p_id, self)
        self.control = {
            "active": [True, self.menu],
            "help": [False, self.instructions_menu],
            "load": [False, self.load_submenu],
            "creator": [False, self.tc]
        }

    def create_menu(self):
        self.background_image()
        thorpy.set_theme("round")
        b_text = ["Start Game", "Load Game", "Instructions", "Quit"]
        buttons = [thorpy.make_button(txt, func=self.menu_func[txt]) for txt in b_text]
        [button.set_font_size(30) for button in buttons]
        [button.scale_to_title() for button in buttons]
        self.menu_box = thorpy.Box(buttons)
        menu = thorpy.Menu(self.menu_box)
        self.proper_display(menu, self.menu_box)
        pg.display.update()
        return menu

    def create_instructions(self):
        self.background_image()
        back = thorpy.Background(color=(0, 0, 0, 0))
        my_reaction = thorpy.ConstantReaction(reacts_to=pg.MOUSEBUTTONDOWN, reac_func=self.exit_instructions)
        back.add_reaction(my_reaction)
        return thorpy.Menu(back)

    def create_load_menu(self):
        self.background_image()
        thorpy.set_theme("round")
        games = self.network.send(["get_games_to_load"])
        load_buttons = [thorpy.make_button(str(game), func=self.load_game, params={"which_game": i, "games": games})
                        for i, game in enumerate(games)]
        quit_button = thorpy.make_button("Quit", func=self.quit_submenu)
        load_buttons.append(quit_button)
        [button.set_font_size(20) for button in load_buttons]
        [button.scale_to_title() for button in load_buttons]
        self.load_box = thorpy.Box(load_buttons)
        load_submenu = thorpy.Menu(self.load_box)
        return load_submenu

    def load_instructions(self):
        self.change_display("help")
        self.draw_image("instructions.png", 50, 50)
        pg.display.update()

    def load_menu(self):
        self.background_image()
        self.change_display("load")
        self.proper_display(self.load_submenu, self.load_box, self.was_loaded)
        self.was_loaded = True
        pg.display.update()

    def load_game(self, which_game, games):
        self.network.send(["load", games[which_game]])
        self.start_game()

    def exit_instructions(self):
        self.change_display("active")
        self.background_image()
        self.menu_box.blit()
        pg.display.update()

    def start_game(self):
        self.network.send(["is_ready", self.p_id, True])
        self.player_ready = True
        self.change_display()

    def quit_submenu(self):
        self.change_display("active")
        self.background_image()
        self.menu_box.blit()
        pg.display.update()

    def highlight_buttons(self, event):
        for con in self.control:
            if self.control[con][0]:
                self.control[con][1].react(event)
                break

    def change_display(self, change=""):
        for key in self.control.keys():
            if key == change:
                self.control[key][0] = True
            else:
                self.control[key][0] = False

    def proper_display(self, menu, box, flag=False):
        if flag is False:
            box.set_main_color((0, 0, 0, 0))
        for element in menu.get_population():
            element.surface = self.window
        box.center()
        box.blit()

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

    def almost_start_game(self):
        self.player_ready = True
        self.control["creator"][0] = True
        self.change_display("creator")

    def team_screen(self):
        self.tc.creator_view()
        pg.display.update()

    def waiting_screen(self):
        self.team_screen() if self.control["creator"][0] else self.loading_screen()
