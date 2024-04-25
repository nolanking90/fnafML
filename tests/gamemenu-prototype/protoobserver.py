import cv2
import mss
import numpy as np
from PIL import Image


def on_game_menu():
    reference = Image.open("left.png")
    reference_gray = cv2.cvtColor(np.array(reference), cv2.COLOR_BGR2GRAY)

    avg_screen_gray = np.zeros_like(reference_gray).astype(float)

    with mss.mss() as sct:
        for _ in range(10):
            screen = sct.grab(sct.monitors[1])
            screen_raw = Image.frombytes("RGB", screen.size, screen.bgra, "raw", "BGRX")

            screen_gray = cv2.cvtColor(np.array(screen_raw), cv2.COLOR_BGR2GRAY)
            avg_screen_gray += screen_gray

    avg_screen_gray /= 10
    avg_screen_gray = avg_screen_gray.astype(np.uint8)

    orb = cv2.ORB_create()

    kp1, des1 = orb.detectAndCompute(reference_gray, None)
    kp2, des2 = orb.detectAndCompute(avg_screen_gray, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    if des1 is None or des2 is None:
        return False

    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    threshold = 200
    is_similar = len(matches) > threshold

    return is_similar

    # leftsimilarity = ssim(screen_gray, reference_gray)
    # cv2.imwrite("avg_screen_gray_game.png", avg_screen_gray)

    # reference = Image.open("right.png")
    # reference_gray = cv2.cvtColor(np.array(reference), cv2.COLOR_BGR2GRAY)
    # rightsimilarity = ssim(screen_gray, reference_gray)
    # cv2.imwrite("avg_screen_gray_game.png", avg_screen_gray)

    # if leftsimilarity > 0.75:
    # return True
    # elif rightsimilarity > 0.75:
    # return True
    # else:
    # return False
