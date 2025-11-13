from dataclasses import dataclass
import numpy as np

import eml4806.geometry.shape as shape

@dataclass
class Chassis:
    length : float = 0.0
    width : float =  0.0
    wheelbase: float = 0.0
    trackwidth: float = 0.0 

@dataclass
class Wheel:
    diameter: float = 0.0  # meters
    width: float = 0.0     # meters

@dataclass
class Motor:
    speed : float = 0.0         # rad/s
    maximum_speed: float = 0.0  # rad/s

@dataclass
class Blade:
    diameter : float = 0.0 # m
    on: bool = False
    height: float = 0.0 # m

@dataclass
class Shape:
    chassis = None
    wheel1 = None
    wheel2 = None
    wheel3 = None
    wheel4 = None
    blade = None

class Robot:
    
    def __init__(self):

        self.chassis = Chassis()
        self.wheel = Wheel()
        self.motor_left = Motor()
        self.motor_right = Motor()
        self.blade = Blade()

        self.maximum_speed = 0.0

        # Graphics
        self.shape = Shape()
   
    def draw(self, ax):
        if self.shape.chassis is None:
            l = self.chassis.length
            w = self.chassis.width
            b = self.chassis.wheelbase
            t = self.chassis.trackwidth
            d = self.wheel.diameter
            s = self.wheel.width
            c = self.blade.diameter

            chassis = shape.box(0.0, 0.0, l, w)
            wheel1 = shape.box(-0.5*b, -0.5*t, d, s)
            wheel2 = shape.box( 0.5*b, -0.5*t, d, s)
            wheel3 = shape.box(-0.5*b,  0.5*t, d, s)
            wheel4 = shape.box( 0.5*b,  0.5*t, d, s)
            blade = shape.circle(0.0, 0.0, 0.5*c)

            (self.shape.chassis,) = ax.fill(chassis[:,0], chassis[:,1], color = (0.0, 0.0, 1.0, 0.2))
            (self.shape.wheel1,) = ax.fill(wheel1[:,0], wheel1[:,1], color = (0.0, 0.0, 1.0, 0.2))
            (self.shape.wheel2,) = ax.fill(wheel2[:,0], wheel2[:,1], color = (0.0, 0.0, 1.0, 0.2))
            (self.shape.wheel3,) = ax.fill(wheel3[:,0], wheel3[:,1], color = (0.0, 0.0, 1.0, 0.2))
            (self.shape.wheel4,) = ax.fill(wheel4[:,0], wheel4[:,1], color = (0.0, 0.0, 1.0, 0.2))
            (self.shape.blade,) = ax.fill(blade[:,0], blade[:,1], color = (0.0, 0.0, 1.0, 0.2))