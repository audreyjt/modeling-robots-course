import math
import numpy as np
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

from eml4806.graphics.style import Style
from eml4806.geometry.transform import Transform

###############################################################


class Shape(ABC):

    def __init__(self, ax, style=Style.default(), transform=Transform.identity()):
        self.ax = ax
        self.style = style
        self._transform = transform

    @property
    def transform(self):
        return self._transform

    @transform.setter
    def transform(self, value):
        self._transform = value    
        self._update()

    @abstractmethod
    def _update(self):
        pass

    

###############################################################

class Rectangle(Shape):

    def __init__(self, ax, width, height, style=Style.default(), transform=Transform.identity()):
        super().__init__(ax, style, transform)
        self.w = width
        self.h = height
        self._make()

    def shape(self):
        w = 0.5*self.w
        h = 0.5*self.h
        return np.array([
            [-w, -h],
            [ w, -h],
            [ w,  h],
            [-w,  h]
        ])

    def _make(self):
        o = self.shape()
        o = self._transform.apply(o)
        self.fill = plt.fill(o[:,0],o[:,1])[0]
        print(self.fill)

    def _update(self):
        print("Rectangle updated!")
        o = self.shape()
        o = self._transform.apply(o)
        self.fill.set_xy(o)

