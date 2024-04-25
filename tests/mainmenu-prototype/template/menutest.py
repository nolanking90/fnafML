import cv2
import mss
import numpy as np
import timeit


def main_menu_template(reference, screen):
    # Template matching
    res = cv2.matchTemplate(screen, reference, cv2.TM_CCOEFF_NORMED)
    threshold = 0.2
    loc = np.where(res >= threshold)
    same = len(loc[0]) > 0
    return same


def get_screen():
    with mss.mss() as sct:
        screen = sct.grab(sct.monitors[1])
    raw = np.array(screen)
    screen_gray = cv2.cvtColor(np.array(raw), cv2.COLOR_BGR2GRAY)
    screen_gray = screen_gray[
        :screen_gray.shape[0] // 2, 50:screen_gray.shape[1] // 2
    ]
    return screen_gray


def run_test(num_frames, trials):
    count = 0
    templatecount = 0
    while count < trials:
        avg_screen = get_screen()
        if main_menu_template(reference, avg_screen):
            templatecount += 1
        count += 1

    return templatecount


reference = cv2.imread("mainmenu.png", cv2.IMREAD_GRAYSCALE)
num_frames = 1
trials = 100
runningp = 0

while True:
    start_time = timeit.default_timer()
    p = run_test(num_frames, trials)
    runningp += p
    end_time = timeit.default_timer()
    print(
        '\033[K'
        + "{:.2f}".format(p / trials * 100) + "%, time: "
        + "{:.3f}".format(end_time - start_time) + " s, "
        + "{:.3f}".format((end_time - start_time)/(trials)) + " s/frame, "
        + "({:})".format(runningp) + " frames matched", end="\r"
    )
