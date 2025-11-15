import numpy as np
import matplotlib.pyplot as plt

from eml4806.geometry.transform import identity
from eml4806.geometry.transform import apply

g_transparency = 0.2

class Shape:
    def __init__(self, axis, shape, color):
        self.color = (color[0], color[1], color[2], g_transparency)
        self.shape = shape
        self.fill = axis.fill(shape[:,0], shape[:,1], self.color)[0]
        
    def update(self, transform = identity()):
        pass
        #shape = apply(self.shape, transform)
        #self.fill.set_data(shape[:,0], shape[:,1])

#######################################################
# Shape generation

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
    a = np.linspace(0.0, 2.0*np.pi, 72)
    x = xc + r*np.cos(a)
    y = yc + r*np.sin(a)
    return np.column_stack((x, y))

    