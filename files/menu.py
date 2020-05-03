import thorpy
import pygame as pg


def my_func():
    print("Please wait for other player...")


def menu_init(window, game_start):
    btn1 = thorpy.make_button("Start Game")
    btn2 = thorpy.make_button("Load Game")
    btn3 = thorpy.make_button("Quit")

    my_reaction = thorpy.ConstantReaction(reacts_to=pg.MOUSEBUTTONDOWN, reac_func=my_func)
    btn1.add_reaction(my_reaction)
    box = thorpy.Box([btn1, btn2])
    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = window

    box.center()
    box.blit()
    box.update()
    return menu
