import cv2
import numpy as np
from mss import mss
import time
import pickle


def record_screen(duration, fps=30):
    sct = mss()
    frames = []
    start_time = time.time()
    while time.time() - start_time < duration:
        ss = np.array(sct.grab(sct.monitors[1]))
        ss = cv2.cvtColor(ss, cv2.COLOR_BGR2GRAY)
        frames.append(ss)
        time.sleep(1.0 / fps)
    return frames


T = 30
frames = record_screen(T)

with open('frames.pkl', 'wb') as f:
    pickle.dump(frames, f)
