import math
import matplotlib.pyplot as plt

import eml4806.graphics.style as stl
import eml4806.geometry.transform as tf

###############################################################


class Shape:
    def __init__(self, ax, transform):
        self.ax = ax
        self.transform = transform

    def show(self):
        if self.patch:
            self.patch.set_visible(True)

    def hide(self):
        if self.patch:
            self.patch.set_visible(False)
        self._draw()

    def color(self, color):
        if self.patch:
            self.patch.set_facecolor(color)
            self.patch.set_edgecolor(color)
        self._draw()

    def opacity(self, value):
        if self.patch:
            self.patch.set_alpha(value)
        self._draw()

    def move(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self._apply_position()
        self._draw()

    def shift(self, dx, dy):
        self.move(self.x + dx, self.y + dy)

    def rotate(self, angle):
        self.a = float(angle)
        self._apply_rotation()
        self._draw()

    @abstractmethod
    def _apply_position(self):
        pass

    @abstractmethod
    def _apply_rotation(self):
        pass


###############################################################


class Circle(Shape):
    def __init__(
        self,
        ax,
        x=0.0,
        y=0.0,
        radius=1.0,
        angle=0.0,
        color="C0",
        opacity=0.7,
        visible=True,
    ):
        super().__init__(ax)
        self.x = float(x)
        self.y = float(y)
        self.r = float(radius)
        self.a = float(angle)
        self.patch = _CirclePatch(
            (self.x, self.y),
            self.r,
            facecolor=color,
            edgecolor=color,
            alpha=opacity,
            visible=visible,
        )
        self.ax.add_patch(self.patch)
        self._draw()

    def _apply_position(self):
        self.patch.center = (self.x, self.y)

    def _apply_rotation(self):
        pass

    def radius(self, value):
        self.r = float(value)
        self.patch.set_radius(self.r)
        self._draw()


###############################################################


class Rectangle(Shape):
    def __init__(
        self,
        ax,
        x=0.0,
        y=0.0,
        width=1.0,
        height=1.0,
        angle=0.0,
        color="C1",
        opacity=0.7,
        visible=True,
    ):
        super().__init__(ax)
        self.x = float(x)
        self.y = float(y)
        self.w = float(width)
        self.h = float(height)
        self.a = float(angle)
        x0 = self.x - self.w / 2.0
        y0 = self.y - self.h / 2.0
        self.patch = _RectPatch(
            (x0, y0),
            self.w,
            self.h,
            facecolor=color,
            edgecolor=color,
            alpha=opacity,
            visible=visible,
        )
        self._update_transform()
        self.ax.add_patch(self.patch)
        self._draw()

    def _update_transform(self):
        t = transforms.Affine2D().rotate_deg_around(self.x, self.y, self.a)
        self.patch.set_transform(t + self.ax.transData)

    def _apply_position(self):
        x0 = self.x - self.w / 2.0
        y0 = self.y - self.h / 2.0
        self.patch.set_xy((x0, y0))
        self._update_transform()

    def _apply_rotation(self):
        self._update_transform()

    def size(self, width, height):
        self.w = float(width)
        self.h = float(height)
        self.patch.set_width(self.w)
        self.patch.set_height(self.h)
        x0 = self.x - self.w / 2.0
        y0 = self.y - self.h / 2.0
        self.patch.set_xy((x0, y0))
        self._update_transform()
        self._draw()


###############################################################


class Group(Shape):
    def __init__(self, shapes, x=0.0, y=0.0, angle=0.0):
        if not shapes:
            raise ValueError("Group requires at least one shape")
        ax = shapes[0].ax
        super().__init__(ax)
        self.shapes = list(shapes)
        self.x = float(x)
        self.y = float(y)
        self.a = float(angle)

    def _apply_position(self):
        for shape in self.shapes:
            dx = self.x - shape.x
            dy = self.y - shape.y
            shape.shift(dx, dy)

    def _apply_rotation(self):
        self._update_children()
