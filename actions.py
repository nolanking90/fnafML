from pynput.mouse import Button, Controller # noqa: F401, E402, E501
import time

main_menu_actions = [
    (185, 418),  # New Game
    (260, 498)   # Continue Game
]

game_menu_actions = [
    (59, 419),    # Left Light
    (57, 334),    # Left Door
    (59, 100),    # Look Left
    (1217, 439),  # Right Light
    (1219, 364),  # Right Door
    (1217, 100),  # Look Right
]


cam_menu_actions = {
    "1a": (993, 358),
    "1b": (966, 410),
    "1c": (930, 491),
    "2a": (991, 608),
    "2b": (976, 645),
    "3": (901, 592),
    "4a": (1083, 601),
    "4b": (1084, 647),
    "5": (858, 437),
    "6": (1185, 570),
    "7": (1191, 437),
}


def click_pos(x: int, y: int):
    mouse = Controller()
    mouse.position = (x, y)
    mouse.click(Button.left, 1)
    time.sleep(.05)


def drag_to_screen():
    mouse = Controller()
    mouse.position = (571, 0)
    mouse.position = (571, 570)
    y = 570
    while y < 690:
        mouse.move(0, 1)
        y += 1


def toggle_screen():
    drag_to_screen()
    click_pos(571, 677)


def toggle_right_light():
    click_pos(1230, 100)  # Look Right
    click_pos(1217, 439)  # Right Light
