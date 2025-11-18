from dataclasses import dataclass
import numpy as np

import eml4806.graphics.shape as shape

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
    maximum_speed: float = 0.0  # rad/s

@dataclass
class Blade:
    diameter : float = 0.0 # m
    on: bool = False
    height: float = 0.0 # m

"""
class Robot:
    def __init__(self, workspace, chassis, wheels, motors, blade):
        self.chassis = chassis
        self.wheels = wheels
        self.motors = motors
        self.blade = blade
        self.shapes = [ 
            shape.Shape(workspace.axis, shape.box(0.0, 0.0, chassis.length, chassis.width), (1.0,1.0,0.0))#,
            #shape.Shape(workspace.axis, shape.box(-0.5*self.chassis.wheelbase, -0.5*self.chassis.trackwidth, self.wheels.diameter, self.wheels.width), (0.5, 0.5, 0.5)),
            #shape.Shape(workspace.axis, shape.box( 0.5*self.chassis.wheelbase, -0.5*self.chassis.trackwidth, self.wheels.diameter, self.wheels.width), (0.5, 0.5, 0.5)),
            #shape.Shape(workspace.axis, shape.box(-0.5*self.chassis.wheelbase,  0.5*self.chassis.trackwidth, self.wheels.diameter, self.wheels.width), (0.5, 0.5, 0.5)),
            #shape.Shape(workspace.axis, shape.box( 0.5*self.chassis.wheelbase,  0.5*self.chassis.trackwidth, self.wheels.diameter, self.wheels.width), (0.5, 0.5, 0.5)),
            #shape.Shape(workspace.axis, shape.circle(0.0,0.0,0.5*self.blade.diameter),(0.0, 0.5, 0.0))
        ]
    def update(self):
        pass
        #for shape in self.shapes:
        #    shape.update()
"""