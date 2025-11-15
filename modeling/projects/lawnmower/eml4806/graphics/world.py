import numpy as np
import matplotlib.pyplot as plt

class Workspace:
    def __init__(self, xmin, xmax, ymin, ymax):
        plt.ion()
        self.figure, self.axis = plt.subplots(figsize=(12, 12))
        self.axis.set_xlim(xmin, xmax)
        self.axis.set_ylim(ymin, ymax)
        self.axis.set_aspect("equal")
        self.axis.grid(True)

    def update(self):
        plt.pause(0.00001)

    def __del__(self):
        plt.ioff()
        plt.show()
    