import cv2 as cv
import mss
import numpy as np
import timeit


def get_screen():
    with mss.mss() as sct:
        screen = sct.grab(sct.monitors[1])
        screen = cv.cvtColor(np.array(screen), cv.COLOR_BGR2RGB)
        screen = screen[:screen.shape[0] // 2, 50:screen.shape[1] // 2]
        return screen


def mse(img, ref):
    err = np.sum((img.astype("float") - ref.astype("float")) ** 2)
    err /= float(img.shape[0] * ref.shape[1])
    return err


def run_test(ref, trials):
    count = 0
    p = 0
    while count < trials:
        img = get_screen()
        assert img is not None, "file could not be read"
        assert ref is not None, "file could not be read"
        assert ref.shape == img.shape, "images are not the same size"
        img_fg = bgrmv(img)
        mse_val = mse(img_fg, reference)
        if mse_val < 1000:
            p += 1
            count += 1
            # print("false positive with mse: {:.2f}".format(mse_val))
        else:
            print("failed with mse: {:.2f}".format(mse_val))
            count += 1

    return p/trials*100


def bgrmv(img):

    mask = np.zeros(img.shape[:2], np.uint8)

    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    rect = (100, 60, 255, 355)

    cv.grabCut(img, mask, rect, bgdModel, fgdModel, 1, cv.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
    img = img * mask2[:, :, np.newaxis]
    return img


reference = cv.imread("ref.png")
trials = 100

for _ in range(5):
    start_time = timeit.default_timer()
    p = run_test(reference, trials)
    end_time = timeit.default_timer()
    print(
        str(p) + "%, time: "
        + "{:.2f}".format(end_time - start_time) + " s, "
        + "{:.2f}".format((end_time - start_time)/trials) + " ~s/frame"
    )
