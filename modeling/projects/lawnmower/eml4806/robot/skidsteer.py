from dataclasses import dataclass
import numpy as np

@dataclass
class Chassis:
    length : float = 0.812
    width : float =  0.421
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

class SkidSteerDrive:
    
    def __init__(self):

        self.chassis = Chassis()
        self.wheel = Wheel()
        self.motor_left = Motor()
        self.motor_right = Motor()
        

        self.wheelbase = 0.54 # m
        self.wheel_diameter = 0.33 # m
        self.wheel_width = 0.114 # m
        self.wheel_maximum_rpm = 116.0
        self.track_width = 0.556 # m
        
        self.weight = 50.0 # Kg
   
    def update():
        pass
