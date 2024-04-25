import cv2
import matplotlib.pyplot as plt
import numpy as np

image = plt.imread("mainmenu.png")
image_gray = image.mean(axis=2)

image_fft_half = np.fft.fft2(image_gray[:, image_gray.shape[1] // 2:])
image_fft_shift_half = np.fft.fftshift(image_fft_half)
image_mag_half = np.abs(image_fft_shift_half)

plt.imshow(
    np.log(image_mag_half),
    cmap="hot",
)
plt.colorbar()
plt.title("2D FFT ")
plt.savefig("heatmap_half.png")
plt.close()

image_fft = np.fft.fft2(image_gray)
image_fft_shift = np.fft.fftshift(image_fft)
image_mag = np.abs(image_fft_shift)

plt.imshow(
    np.log(image_mag),
    cmap="hot",
)

plt.colorbar()
plt.title("2D FFT ")
plt.savefig("heatmap.png")
plt.close()

threshold = 10
noise_mask = image_mag > threshold
plt.imshow(
    noise_mask,
    cmap="gray",
)
plt.title("Noise Mask")
plt.colorbar()
plt.savefig("noise_mask.png")
plt.close()

# For comparison, let's window the image before computing the PSD
window_row = np.hamming(image_gray.shape[0])[:, np.newaxis]
window_col = np.hamming(image_gray.shape[1])[np.newaxis, :]
window_2d = window_row * window_col
image_windowed = image_gray * window_2d
image_fft_win = np.fft.fft2(image_windowed)
image_fft_shift_win = np.fft.fftshift(image_fft_win)
image_mag_win = np.abs(image_fft_shift_win)
# image_psd = np.square(image_mag)
# image_psd = image_psd[: image_psd.shape[0] // 2, : image_psd.shape[1] // 2]

plt.imshow(
    np.log(image_mag_win),
    cmap="hot",
)

plt.colorbar()
plt.title("2D FFT (windowed)")
plt.savefig("heatmap_windowed.png")
plt.close()

# Apply a threshold to the PSD to identify noise.
noise_mask = image_mag_win > threshold
plt.imshow(
    noise_mask,
    cmap="hot",
)
plt.colorbar()
plt.title("Noise Mask (windowed)")
plt.savefig("noise_mask_windowed.png")
plt.close()

# Filtering
mask = np.ones_like(image_gray)
center = (640, 360)
axes_outer = (20, 50)
axes_inner = (5, 5)
angle = 0
startAngle = 0
endAngle = 360
color = 0
cv2.ellipse(mask, center, axes_outer, angle, startAngle, endAngle, color, -1)
cv2.ellipse(mask, center, axes_inner, angle, startAngle, endAngle, 1, -1)

psd_noise = np.abs(image_fft_shift_half) ** 2
noise_model = psd_noise / np.sum(psd_noise)
noise_model_resized = cv2.resize(
    noise_model, (image_fft_shift.shape[1], image_fft_shift.shape[0])
)
filtered_fft = image_fft_shift * (1 - noise_model_resized)
filtered_image = np.fft.ifft2(np.fft.ifftshift(filtered_fft))
plt.imsave("filtered_menu.png", np.abs(filtered_image), cmap="gray")

# filtered_fft = image_fft_shift
# filtered_image_mag = np.abs(filtered_fft)
# plt.imshow(
# np.log(filtered_image_mag),
# cmap="hot",
# )
# plt.colorbar()
# plt.savefig("filtered_heatmap.png")

# filtered_image = np.fft.ifft2(np.fft.ifftshift(filtered_fft))
# plt.imsave("filtered_menu.png", np.abs(filtered_image), cmap="gray")
