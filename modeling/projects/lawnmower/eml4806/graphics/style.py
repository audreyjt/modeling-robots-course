from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

#######################################################


@dataclass
class Color:

    r: float
    g: float
    b: float

    def tuple(self):
        return (self.r, self.g, self.b)

    def clone(self):
        return Color(r=self.r, g=self.g, b=self.b)


#######################################################


@dataclass
class Stroke:

    color: Color
    width: float = 1.0

    def clone(self):
        return Stroke(color=self.color, width=self.width)


#######################################################


@dataclass
class Fill:

    color: Color

    def clone(self):
        return Fill(color=self.color)


#######################################################


@dataclass
class Style:

    stroke: Optional[Stroke] = None
    fill: Optional[Fill] = None
    opacity: float = 1.0

    @property
    def has_fill(self) -> bool:
        return self.fill is not None and self.opacity > 0.0

    @property
    def has_stroke(self) -> bool:
        return (
            self.stroke is not None and self.opacity > 0.0 and self.stroke.width > 0.0
        )

    def clone(self):
        return Style(
            stroke=self.stroke.clone() if self.stroke is not None else None,
            fill=self.fill.clone() if self.fill is not None else None,
            opacity=self.opacity,
        )

    @classmethod
    def default(cls):
        color = Color(1.0, 0.0, 0.0)
        return cls(stroke=Stroke(color, 1.0), fill=Fill(color), opacity=0.5)
