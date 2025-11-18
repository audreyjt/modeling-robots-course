# Simulate a particle moving around a circle.

import numpy as np
import matplotlib.pyplot as plt

import eml4806.geometry.angle as angle
import eml4806.geometry.vector as vector
import eml4806.sensor.keyboard as keyboard
import eml4806.robot.skidsteer as skidsteer


from eml4806.graphics.workspace import Workspace
from eml4806.graphics.shape import Rectangle, Circle, Polyline, Group
from eml4806.graphics.style import Color, Style
from eml4806.geometry.transform import Transform

def main():

    # Land
    xmin = -1.0
    xmax = 10.0
    ymin = -1.0
    ymax = 10.0
    
    workspace = Workspace(xmin, xmax, ymin, ymax)

    # Robot
    # ClearPath Husky A200 Ground Platform
    # https://docs.clearpathrobotics.com/docs_robots/outdoor_robots/husky/a200/user_manual_husky/

    chassis = skidsteer.Chassis()
    chassis.length     = 0.812 # m
    chassis.width      = 0.421 # m
    chassis.wheelbase  = 0.512 # m
    chassis.trackwidth = 0.550 # m

    wheels = skidsteer.Wheel()
    wheels.diameter = 0.330 # m
    wheels.width    = 0.114 # m
    
    motors = skidsteer.Motor()
    motors.maximum_speed = 5.450 # rad/s (~52 rpm maximum)
        
    blade = skidsteer.Blade()
    blade.diameter = 0.9*chassis.width # m
    blade.height   = 0.05 # m (~2 inches)

    # Robot parts
    body = Rectangle(workspace, 0.0, 0.0, chassis.length, chassis.width, style=Style.brush(Color(1.0,0.55,0.0), 0.5))
    wheel1 = Rectangle(workspace, -0.5*chassis.wheelbase, -0.5*chassis.trackwidth, wheels.diameter, wheels.width, style=Style.brush(Color(0.5,0.5,0.5), 0.5))
    wheel2 = Rectangle(workspace,  0.5*chassis.wheelbase, -0.5*chassis.trackwidth, wheels.diameter, wheels.width, style=Style.brush(Color(0.5,0.5,0.5), 0.5))
    wheel3 = Rectangle(workspace, -0.5*chassis.wheelbase,  0.5*chassis.trackwidth, wheels.diameter, wheels.width, style=Style.brush(Color(0.5,0.5,0.5), 0.5))
    wheel4 = Rectangle(workspace,  0.5*chassis.wheelbase,  0.5*chassis.trackwidth, wheels.diameter, wheels.width, style=Style.brush(Color(0.5,0.5,0.5), 0.5))
    tool = Circle(workspace, 0.0, 0.0, 0.5*blade.diameter, style=Style.brush(Color(1.0,0.0,0.0), 0.5))
    
    # Robot assembly
    robot = Group([body, wheel1, wheel2, wheel3, wheel4, tool])
    
    # Robot path
    path = Polyline(workspace, style=Style.pen(Color(0.0,0.0,1.0)))

    # Initial pose
    x0 = 0.0 # m
    y0 = 0.0 # m
    theta0 = np.deg2rad(10.0) # rad

    tf_robot = Transform(position=(x0, y0), orientation=theta0)
    robot.setTransform(tf_robot)

    path.append( [x0, y0] )

    # Kinematics
    v = 0.0 # m/s
    w = 0.0 # rad/s

    # Controller sensitivity
    dt = 1.0 # s
    dv = 0.01 # m/s
    dw = 0.01 # rad/s

    # Robot specifications
    vmax = 1.0   # m/s
    wmax = 2.0*np.pi # rad/s
        
    # Simulation
    t = 0.0 # s
    dt = 0.1 # s

    # Pose
    x = x0
    y = y0
    theta = theta0

    while True:
        
        # Input
        key = keyboard.key()

        # Commands
        if key == 'q':
            break
        elif key == 'up':
            v += dv
            w = 0.0
        elif key == 'down':
            v -= dv
            w = 0.0
        elif key == 'right':
            w -= dw
        elif key == 'left':
            w += dw
        elif key == ' ':
            v = 0.0
            w = 0.0
                
        # Physics constraints
        v = np.clip(v, -vmax, vmax)
        w = np.clip(w, -wmax, wmax)

        # Digital odometric localization
        x = x + v*dt*np.cos(theta)
        y = y + v*dt*np.sin(theta)
        theta = theta + w*dt

        # Workspace constraints (geofencing)
        x = np.clip(x, 0.98*xmin, 0.98*xmax)
        y = np.clip(y, 0.98*ymin, 0.98*ymax)
        tetha = angle.normalize(theta)

        # Update robot location
        tf_robot = Transform(position=[x,y], orientation=theta)
        robot.setTransform(tf_robot)

        # Update path (only if the robot position changed!)
        if not vector.coincident([x,y], path.last(), tol=0.001):
            path.append( [x,y] )

        # Simulation
        workspace.update()
        t = t + dt
    
    print("Bye!")

if __name__ == "__main__":
    main()
