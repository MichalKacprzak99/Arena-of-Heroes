import thorpy
import pygame as pg
from settings import load_image, game_settings


class Menu:
    def __init__(self, window):
        self.window = window
        self.buttons = []
        self.b_text = ["Start Game", "Load Game", "Instructions", "Quit"]
        self.box = None
        self.menu = self.create()
        self.player_ready = False
        self.opponent_ready = False
        self.active = True
        self.help = False

    def create(self):
        self.background_image()

        thorpy.set_theme("round")
        self.buttons = [thorpy.make_button(txt) for txt in self.b_text]
        [button.set_font_size(30) for button in self.buttons]
        [button.scale_to_title() for button in self.buttons]
        self.buttons[1].active = False
        self.box = thorpy.Box(self.buttons)
        menu = thorpy.Menu(self.box)
        self.box.set_main_color((0, 0, 0, 0))
        for element in menu.get_population():
            element.surface = self.window

        self.box.center()
        self.box.blit()

        pg.display.update()

        return menu

    def click(self, mouse, network, p_id):
        if self.help is True:
            self.help = False
            self.active = True
            self.background_image()
            self.box.blit()
            pg.display.update()
        else:
            for element in self.menu.get_population():
                if element.get_rect().collidepoint(mouse) and self.player_ready is False:
                    if element.get_full_txt() == "Start Game":
                        network.send(["is_ready", p_id, True])
                        self.player_ready = True
                        self.active = False
                    elif element.get_full_txt() == "Load Game":
                        pass
                    elif element.get_full_txt() == "Instructions":
                        self.instructions()
                    elif element.get_full_txt() == "Quit":
                        pg.quit()

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
        self.draw_text("Game will start soon", 300, 200, 23)
        pg.display.update()

    def instructions(self):
        self.active = False
        self.help = True
        pg.draw.rect(self.window, (0, 0, 240),
                     (50, 50, game_settings["GAME_SCREEN_WIDTH"] -100, game_settings["GAME_SCREEN_HEIGHT"]-300))
        pg.draw.rect(self.window, (0, 0, 190),
                     (50, 50, game_settings["GAME_SCREEN_WIDTH"] -100, game_settings["GAME_SCREEN_HEIGHT"]-300), 5)
        self.draw_text("Choose your team and battle with them in Arena of Heroes!", 70, 70)
        self.draw_text("Main goal of the game is to defeat all of your opponent heroes before them!", 70, 100)
        self.draw_text("Here's brief description of every class:", 230, 130)
        self.draw_image("ARCHER\south.png", 70, 160)
        self.draw_text("Archer can move fast and attack from far distance with arrows.", 130, 180)
        self.draw_image("HEALER\south.png", 70, 230)
        self.draw_text("Healer can keep your characters alive when needed.", 130, 250)
        self.draw_image("MAGE\south.png", 70, 300)
        self.draw_text("Mage can cast strong magic spells on your enemies.", 130, 320)
        self.draw_image("HERO\south.png", 70, 370)
        self.draw_text("Warrior can dish out heavy damage in close range attacks.", 130, 390)
        self.draw_text("Click anywhere to go back", 300, 450)
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
