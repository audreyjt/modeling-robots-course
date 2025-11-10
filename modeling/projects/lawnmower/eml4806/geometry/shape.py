import numpy as np

def box(x, y, w, h):
    w = 0.5*w
    h = 0.5*h
    return np.array([
        [x - w, y - h],  # bottom-left
        [x + w, y - h],  # bottom-right
        [x + w, y + h],  # top-right
        [x - w, y + h],  # top-left
    ], dtype=float)
