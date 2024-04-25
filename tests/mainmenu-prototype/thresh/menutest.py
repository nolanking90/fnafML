import cv2
import mss
import numpy as np
import timeit


# didn't work very well
def main_menu_thresh(reference, screen, kernel):
    # Threshold for similarity
    _, tref = cv2.threshold(reference, 128, 255, cv2.THRESH_BINARY)
    _, tscreen = cv2.threshold(screen, 128, 255, cv2.THRESH_BINARY)

    tref = cv2.morphologyEx(tref, cv2.MORPH_CLOSE, kernel)
    tscreen = cv2.morphologyEx(tscreen, cv2.MORPH_CLOSE, kernel)

    same = np.array_equal(tref, tscreen)
    # cv2.imwrite("thresh/tref.png", tref)
    # cv2.imwrite("thresht/screen" + str(count) + ".png", tscreen)
    return same


def get_avg_screen(reference, num_frames):
    avg_screen = np.zeros_like(reference).astype(float)

    with mss.mss() as sct:
        for _ in range(num_frames):
            screen = sct.grab(sct.monitors[1])
            raw = np.array(screen)
            screen_gray = cv2.cvtColor(np.array(raw), cv2.COLOR_BGR2GRAY)
            screen_gray = screen_gray[
                :screen_gray.shape[0] // 2, 50:screen_gray.shape[1] // 2
            ]
            avg_screen += screen_gray

        avg_screen /= num_frames
        avg_screen = avg_screen.astype(np.uint8)
        return avg_screen


def run_test(num_frames, trials):
    count = 0
    threshcount = 0
    while count < trials:
        avg_screen = get_avg_screen(reference, num_frames)
        result = main_menu_thresh(
            reference,
            avg_screen,
            np.ones((5, 5), np.uint8)
            ) | main_menu_thresh(
            reference,
            avg_screen,
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            ) | main_menu_thresh(
            reference,
            avg_screen,
            cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
            )
        if result:
            threshcount += 1
        count += 1

    return threshcount/count*100


reference = cv2.imread("mainmenu.png", cv2.IMREAD_GRAYSCALE)
num_frames = 5
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
