# Simulate a particle moving around a circle.

import numpy as np
import matplotlib.pyplot as plt

import eml4806.geometry.angle as angle
import eml4806.sensor.keyboard as keyboard
import eml4806.robot.skidsteer as skidsteer

def main():
    
    # Robot
    # ClearPath Husky A200 Ground Platform
    # https://docs.clearpathrobotics.com/docs_robots/outdoor_robots/husky/a200/user_manual_husky/

    robot = skidsteer.Robot()

    robot.maximum_speed = 1.0 # m/s

    robot.chassis.length = 0.812 # m
    robot.chassis.width = 0.421 # m
    robot.chassis.wheelbase = 0.512 # m
    robot.chassis.trackwidth = 0.550 # m

    robot.wheel.diameter = 0.330 # m
    robot.wheel.width = 0.114 # m

    robot.motor_left.maximum_speed = 5.45 # rad/s (52 rpm maximum!)
    robot.motor_right.maximum_speed = 5.45 # rad/s (52 rpm maximum!)

    robot.blade.diameter = 0.9*robot.chassis.width # m
    robot.blade.height = 0.05 # m (2 inches)

    # Robot initial condition    
    x = 0.0 # m
    y = 0.0 # m
    theta = np.pi/2.0 # rad

    # Simulation
    t = 0.0 # s
    dt = 1.0 # s

    # Workspace
    xmin = -1.0
    xmax = 10.0
    ymin = -1.0
    ymax = 10.0
   
    # Create graphics
    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.grid(True)

    while True:

        # Commands
        key = keyboard.key()

        if key == 'q':
            break
                
        # Update graphics
        robot.draw(ax)
        fig.supxlabel(f't: {t}')
        plt.pause(0.00001)

        # Step simulation foward
        t = t + dt

    plt.ioff()
    plt.show()
    
    print("Bye!")

if __name__ == "__main__":
    main()
