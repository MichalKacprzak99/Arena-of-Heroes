import thorpy


class Menu:
    def __init__(self, window):
        self.window = window
        self.buttons = []
        self.b_text = ["Start Game", "Load Game", "Instructions", "Quit"]
        self.menu = self.create()
        self.active = True

    def create(self):
        thorpy.set_theme("round")
        self.buttons = [thorpy.make_button(txt) for txt in self.b_text]
        box = thorpy.Box(self.buttons)
        menu = thorpy.Menu(box)
        for element in menu.get_population():
            element.surface = self.window
        box.center()
        box.blit()
        box.update()
        return menu

    def click(self, mouse, network, p_id):
        for element in self.menu.get_population():
            if element.get_rect().collidepoint(mouse):
                if element.get_full_txt() == "Start Game":
                    network.send(["is_started", p_id, True])
                    return True
                elif element.get_full_txt() == "Load Game":
                    pass
                elif element.get_full_txt() == "Instructions":
                    pass
                elif element.get_full_txt() == "Quit":
                    pass
        return False
