import time
import ctypes
import os

import cv2
import numpy as np

from actions import click_pos


def get_screen(sct):
    screen = sct.grab(sct.monitors[1])
    raw = np.array(screen)
    screen_gray = cv2.cvtColor(np.array(raw), cv2.COLOR_BGR2GRAY)
    return screen_gray


def main_menu_template(reference, screen):
    screen = screen[: screen.shape[0] // 2, 50 : screen.shape[1] // 2]
    res = cv2.matchTemplate(screen, reference, cv2.TM_CCOEFF_NORMED)
    threshold = 0.2
    loc = np.where(res >= threshold)
    same = len(loc[0]) > 0
    return same


def lore_match_template(reference, screen):
    res = cv2.matchTemplate(screen, reference, cv2.TM_CCOEFF_NORMED)
    threshold = 0.25
    loc = np.where(res >= threshold)
    same = len(loc[0]) > 0
    return same


def cam_match_template(reference, screen):
    screen = screen[330:, 825:]
    res = cv2.matchTemplate(screen, reference, cv2.TM_CCOEFF_NORMED)
    threshold = 0.45
    loc = np.where(res >= threshold)
    same = len(loc[0]) > 0
    return same


def trans_match_template(reference, screen):
    screen = screen[180:540, 320:960]
    res = cv2.matchTemplate(screen, reference, cv2.TM_CCOEFF_NORMED)
    threshold = 0.5
    loc = np.where(res >= threshold)
    same = len(loc[0]) > 0
    return same


def match_template(reference, screen):
    res = cv2.matchTemplate(screen, reference, cv2.TM_CCOEFF_NORMED)
    threshold = 0.45
    loc = np.where(res >= threshold)
    same = len(loc[0]) > 0
    return same


def game_match_template(reference, screen):
    screen = screen[100:200,:]
    res = cv2.matchTemplate(screen, reference, cv2.TM_CCOEFF_NORMED)
    threshold = 0.5
    loc = np.where(res >= threshold)
    same = len(loc[0]) > 0
    # cv2.imwrite("game.png", screen)
    return same


def get_l_door(sct, delay):
    click_pos(50, 100)  # Look Left
    time.sleep(delay)
    click_pos(50, 100)  # Look Left
    screen = get_screen(sct)
    door = screen[175:405, 100:280]
    win = screen[210:400, 400:515]
    # cv2.imwrite("ldoor.png", door)
    # cv2.imwrite("lwin.png", win)
    return door, win


def get_r_door(sct, delay):
    click_pos(1230, 100)  # Look Right
    time.sleep(delay)
    click_pos(1230, 100)  # Look Right
    screen = get_screen(sct)
    door = screen[155:465, 990:1150]
    win = screen[200:510, 725:885]
    # cv2.imwrite("rdoor.png", door)
    # cv2.imwrite("rwin.png", win)
    return door, win


def get_cam(cam):
    pass


def get_power():
    pid = 523058
    address1 = 0x000000000060fc98
    address2 = 0x000000000060fca4
    # address3 = 0x000000000060fcd0
    # address4 = 0x000000000060fd50
    libc = ctypes.CDLL('libc.so.6')
    ptrace = libc.ptrace
    ptrace.restype = ctypes.c_long
    ptrace.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]

    ptrace(16, pid, None, None)
    os.waitpid(pid, 0)
    value1 = ptrace(1, pid, address1, None)
    value2 = ptrace(1, pid, address2, None)
    # value3 = ptrace(1, pid, address3, None)
    # value4 = ptrace(1, pid, address4, None)

    # address5 = value1+value2
    # address6 = value1+value4

    # value5 = ptrace(1, pid, address5, None)
    # value6 = ptrace(1, pid, address6, None)

    ptrace(17, pid, None, None)

    return value1, value2

    # return power, utiliization
