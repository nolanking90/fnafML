import argparse

import cv2 as cv
import numpy as np
from skimage.metrics import mean_squared_error as skmse


def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


def ssim(imageA, imageB):
    mu_A = cv.mean(imageA)[0]
    mu_B = cv.mean(imageB)[0]
    sigma_A = cv.meanStdDev(imageA)[1][0][0]
    sigma_B = cv.meanStdDev(imageB)[1][0][0]
    covariance = (np.mean(imageA * imageB) - mu_A * mu_B) / 255.0
    ssim = ((2 * mu_A * mu_B + 1.0) * (2 * covariance + 1.0)) / (
        (mu_A**2 + mu_B**2 + 1.0) * (sigma_A**2 + sigma_B**2 + 1.0)
    )
    return ssim


parser = argparse.ArgumentParser()
parser.add_argument("n", type=int, help="The number of iterations.")
args = parser.parse_args()
n = args.n

img = cv.imread("mainmenu.png")
img = img[:img.shape[0] // 2, 50:img.shape[1] // 2]
ref = cv.imread("ref.png")

assert img is not None, "file could not be read, check with os.path.exists()"
assert ref is not None, "file could not be read, check with os.path.exists()"
assert ref.shape == img.shape, "images are not the same size"

mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
rect = (100, 60, 255, 355)

cv.grabCut(img, mask, rect, bgdModel, fgdModel, n, cv.GC_INIT_WITH_RECT)

mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
img = img * mask2[:, :, np.newaxis]

cv.imwrite("grabcut.png", img)
print(f"{n} iteration:")
print(f"MSE: {mse(img, ref)}, SSIM: {ssim(img, ref)}")
print(f"MSE: {skmse(img, ref)}")

img = cv.imread("left.png")
img = img[:img.shape[0] // 2, 50:img.shape[1] // 2]
ref = cv.imread("ref.png")

assert img is not None, "file could not be read, check with os.path.exists()"
assert ref is not None, "file could not be read, check with os.path.exists()"
assert ref.shape == img.shape, "images are not the same size"

mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
rect = (100, 60, 255, 355)

cv.grabCut(img, mask, rect, bgdModel, fgdModel, n, cv.GC_INIT_WITH_RECT)

mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
img = img * mask2[:, :, np.newaxis]

cv.imwrite("grabcut.png", img)
print(f"{n} iteration:")
print(f"MSE: {mse(img, ref)}, SSIM: {ssim(img, ref)}")
print(f"MSE: {skmse(img, ref)}")
