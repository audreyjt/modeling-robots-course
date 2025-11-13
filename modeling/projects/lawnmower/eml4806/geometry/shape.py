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

def circle(xc, yc, r):
    t = np.linspace(0.0, 2.0*np.pi, 72)
    x = xc + r*np.cos(t)
    y = yc + r*np.sin(t)
    return np.column_stack((x, y))

    