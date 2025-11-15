# Simulate a particle moving around a circle.

import numpy as np
import matplotlib.pyplot as plt

import eml4806.geometry.angle as angle
import eml4806.graphics.world as world
import eml4806.sensor.keyboard as keyboard
import eml4806.robot.skidsteer as skidsteer


def main():

    # Land
    xmin = -1.0
    xmax = 10.0
    ymin = -1.0
    ymax = 10.0
    
    workspace = world.Workspace(xmin, xmax, ymin, ymax)

    # Robot
    # ClearPath Husky A200 Ground Platform
    # https://docs.clearpathrobotics.com/docs_robots/outdoor_robots/husky/a200/user_manual_husky/

    chassis = skidsteer.Chassis(   
        0.812, # Length (m),
        0.421, # Width (m),
        0.512, # Wheelbase (m)
        0.550  # Trackwidth (m)
    )

    wheels = skidsteer.Wheel(
        0.330, # Diameter (m)
        0.114  # Width (m)
    )

    motors = skidsteer.Motor(
        5.450 # Maximum speed (rad/s), ~52 rpm maximum!
    )
    
    blade = skidsteer.Blade(
        0.9*chassis.width, # Diameter (m)
        0.05               # Height (m), ~2 inches!
    )

    robot = skidsteer.Robot(workspace, chassis, wheels, motors, blade)
    
    # Simulation
    t = 0.0 # s
    dt = 0.1 # s

    while True:
        # Commands
        key = keyboard.key()

        if key == 'q':
            break
                
        # Update graphics
        robot.update()
        workspace.update()
        
        # Step simulation foward
        t = t + dt
    
    print("Bye!")

if __name__ == "__main__":
    main()
