# Simulate a particle moving around a circle.
# Lawn mower robot
# https://youtu.be/2Rhsv8fFqCE

import numpy as np
import matplotlib.pyplot as plt

import eml4806.geometry.angle as angle

import eml4806.sensor.keyboard as keyboard

from eml4806.geometry.vector import vector
from eml4806.graphics.workspace import Workspace
from eml4806.graphics.shape import Rectangle, Circle, Polyline, Group, Vector
from eml4806.graphics.style import Color, Style
from eml4806.geometry.transform import Transform
from eml4806.robot.odometry import AnalyticalSkidDriveOdometer
from eml4806.robot.skidsteer import Chassis, Wheel, Motor, Blade, Robot

def main():

    # Land
    xmin = -1.0
    xmax = 10.0
    ymin = -1.0
    ymax = 10.0

    workspace = Workspace(xmin, xmax, ymin, ymax)

    # Robot docking station
    x0 = 0.0  # m
    y0 = 0.0  # m
    theta0 = np.deg2rad(10.0)  # rad

    dock = Circle(workspace, x0, y0, 0.1, style=Style.brush(Color(1.0, 0.0, 1.0)))

    # Robot physics
    # ClearPath Husky A200 Ground Platform
    # https://docs.clearpathrobotics.com/docs_robots/outdoor_robots/husky/a200/user_manual_husky/

    chassis = Chassis()
    chassis.length = 0.812  # m
    chassis.width = 0.421  # m
    chassis.wheelbase = 0.512  # m
    chassis.trackwidth = 0.550  # m

    wheels = Wheel()
    wheels.diameter = 0.330  # m
    wheels.width = 0.114  # m

    motors = Motor()
    motors.maximum_angular_velocity = 5.45  # rad/s (~52 rpm maximum)

    blade = Blade()
    blade.diameter = 0.9 * chassis.width  # m
    blade.height = 0.05  # m (~2 inches)

    odometer = AnalyticalSkidDriveOdometer()
    odometer.track_width = chassis.trackwidth
    odometer.maximum_linear_velocity = 1.0  # m/s
    odometer.maximum_angular_velocity = 3.5  # rad/s

    # Simulated robot
    robot = Robot(workspace, x0, y0, theta0, chassis, wheels, motors, blade, odometer)

    # Direct wheel-speed control modeling a microcontroller-style PWM motor driver
    wl = 0.0  # Left wheel speed  (rad/s)
    wr = 0.0  # Right wheel speed (rad/s)

    # Controller sensitivity
    dv = 0.20  # rad/s, Linear velocity increase
    dw = 0.15  # rad/s, Angular velocity increse 

    # Simulation
    t = 0.0 # s
    dt = 0.02 # s (~50 Hz)

    while True:

        # Input
        key = keyboard.key()

        # Commands inside the microntroller
        if key == "q":
            break
        elif key == "up":
            wl += dv
            wr += dv
        elif key == "down":
            wl -= dv
            wr -= dv
        elif key == "left":
            wl -= dw
            wr += dw
        elif key == "right":
            wl += dw
            wr -= dw
        elif key == " ":
            wl = 0.0
            wr = 0.0

        # Motors physical limits
        wl = np.clip(wl, -motors.maximum_angular_velocity, motors.maximum_angular_velocity)
        wr = np.clip(wr, -motors.maximum_angular_velocity, motors.maximum_angular_velocity)

        # Sensor
        x, y = robot.gps()

        # Controller
        # ...

        # Actuator
        robot.move(t, wl, wr)  # Actuator
        
        # Update scene
        workspace.update()

        # Advance time
        t = t + dt

    print("Bye!")

if __name__ == "__main__":
    main()
