import cv2
import mss
import time

from actions import click_pos, main_menu_actions
from observer import (
    cam_match_template,
    game_match_template,
    get_l_door,
    get_r_door,
    get_screen,
    lore_match_template,
    main_menu_template,
    match_template,
    trans_match_template,
    get_power,
)

mmref = cv2.imread("tests/references/mainmenuref.png", cv2.IMREAD_GRAYSCALE)
loreref = cv2.imread("tests/references/loreref.png", cv2.IMREAD_GRAYSCALE)
gamerefl = cv2.imread("tests/references/gamerefl.png", cv2.IMREAD_GRAYSCALE)
gamerefr = cv2.imread("tests/references/gamerefr.png", cv2.IMREAD_GRAYSCALE)
loadref = cv2.imread("tests/references/loadingref.png", cv2.IMREAD_GRAYSCALE)
camref = cv2.imread("tests/references/camscreenref.png", cv2.IMREAD_GRAYSCALE)
transref = cv2.imread("tests/references/transition.png", cv2.IMREAD_GRAYSCALE)

sct = mss.mss()
delay = 0.80
oldval = 100

while True:
    screen = get_screen(sct)
    if main_menu_template(mmref, screen):
        print("main menu")
        click_pos(*main_menu_actions[0])  # Click New Game
        time.sleep(5)
    elif match_template(loadref, screen):
        print("\033[Kloading screen", end="\r")
    elif game_match_template(gamerefl, screen):
        val1, val2 = get_power()
        val1 = (val1 & 0xffff)
        val2 = (val2 & 0xffff)
        print(val1 & 0xff)
        if ( val1 == val2 
            and (val1 & 0xff) <= oldval 
            and (val1 & 0xff) > oldval - 10
        ):
            print("game menu (l)")
            print(val1 & 0xff)
            oldval = val1 & 0xff

        get_l_door(sct, 0)
        click_pos(57, 334)  # Left Door
        time.sleep(2)
        # click_pos(57, 334)  # Left Door
        # get_r_door(sct, delay)
        # click_pos(1219, 364)  # Right Door
        # break
    elif game_match_template(gamerefr, screen):
        val1, val2 = get_power()
        val1 = (val1 & 0xffff)
        val2 = (val2 & 0xffff)
        if val1 == val2 and (
            (val1 & 0xff) == (oldval - 1) or (val1 & 0xff) == oldval
        ):
            print("game menu (r)")
            # print(val1 & 0xff)
            oldval = val1 & 0xff

        # get_r_door(sct, 0)
        # get_l_door(sct, delay)
        # break
    elif lore_match_template(loreref, screen):
        print("\033[Klore screen", end="\r")
        click_pos(*main_menu_actions[0])  # Click New Game
        time.sleep(5)
    elif cam_match_template(camref, screen):
        print("cam menu")
    elif trans_match_template(transref, screen):
        print("\033[KTransisiton Screen", end="\r")
    else:
        print("\033[KUnkown Screen", end="\r")
