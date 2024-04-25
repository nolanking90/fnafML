import numpy as np
import matplotlib.pyplot as plt
import pickle


def plot_fft(frames, rows):
    power_spectra = [
        np.abs(np.fft.fft(frame))**2 for frame in np.array(frames)[:, rows, :]
    ]

    plt.figure(figsize=(10, 6))
    plt.imshow(np.log(power_spectra), aspect='auto', cmap='hot')
    plt.colorbar(label='Log Power Spectrum')
    plt.ylabel('Row')
    plt.xlabel('Frequency')
    plt.title('Power Spectrum of Rows')
    plt.show()


rows = range(100, 110)
with open('frames.pkl', 'rb') as f:
    frames = pickle.load(f)

plot_fft(frames, rows)
