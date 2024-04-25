import cv2
import timeit
from observers import main_menu_template, get_screen


def run_test(num_frames, trials):
    count = 0
    templatecount = 0
    while count < trials:
        avg_screen = get_screen()
        if main_menu_template(reference, avg_screen):
            templatecount += 1
        count += 1

    return templatecount


reference = cv2.imread("references/mainmenuref.png", cv2.IMREAD_GRAYSCALE)
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
