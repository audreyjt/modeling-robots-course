from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

#######################################################

class Color:

    def __init__(self, r: float = 0.0, g: float = 0.0, b: float = 1.0):
        self.color = (r, g, b)
    
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


class Style:

    def __init__(self, stroke: Stroke = None, fill: Fill = None, opacity = 0.5):
        self.stroke = stroke
        self.fill = fill
        self.opacity = float(opacity)

    def has_fill(self):
        return self.fill is not None and self.opacity > 0.0

    def has_stroke(self):
        return (self.stroke is not None and self.opacity > 0.0 and self.stroke.width > 0.0)

    def clone(self):
        return Style(
            stroke=self.stroke.clone() if self.stroke is not None else None,
            fill=self.fill.clone() if self.fill is not None else None,
            opacity=self.opacity,
        )

    @classmethod
    def pen(cls, color, opacity = 1.0):
        return cls(stroke=Stroke(color), opacity=opacity)
    
    @classmethod
    def brush(cls, color, opacity = 1.0):
        return cls(stroke=Stroke(color), fill=Fill(color), opacity=opacity)

    @classmethod
    def defaultPen(cls):
        return cls.pen(Color(0.0, 1.0, 0.0))
        
    @classmethod
    def defaultBrush(cls):
        return cls.brush(Color(1.0,0.0,1.0))
    