# Simulate a particle moving around a circle.

import numpy as np
import matplotlib.pyplot as plt
import eml4806.input as inp

from eml4806.robot.skidsteer import SkidSteerDrive

def main():
    
    # Robot: ClearPath Husky A200 Ground Platform
    robot = SkidSteerDrive()
    robot.chassis.length = 0.812
    robot.chassis.width = 0.421
    robot.chassis.wheelbase = 0.54
    robot.chassis.trackwidth = 0.556

    robot.wheel.diameter = 0.33
    robot.wheel.width = 0.114

    robot.motor_left.maximum_speed = 5.45 # rad/s (52 rpm maximum!)
    robot.motor_right.maximum_speed = 5.45 # rad/s (52 rpm maximum!)

    robot.weight = 50.0

    # Robot initial condition    
    x = 0.0 # m
    y = 0.0 # m
    theta = np.pi/2.0 # rad

    # Kinematics
    v = 0.0 # m/s
    w = 0.0 # rad/s
    
    # Simulation
    dt = 1.0 # s
    dv = 0.01 # m/s
    dw = 0.001 # rad/s

    # Robot specifications
    vmax = 1.0   # m/s
    wmax = 2.0*np.pi # rad/s
    
    # Workspace
    xmin = -100.0
    xmax =  100.0
    ymin = -100.0
    ymax =  100.0
   
    # Decoration
    trail_size = 500
    trail_x = np.array([x])
    trail_y = np.array([y])

    # Create graphics
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.grid(True)

    # Draw robot
    (trail,) = ax.plot([x], [y], "-", linewidth=3.0, alpha=0.5, label="trail")
    (particle,) = ax.plot(trail_x, trail_y, "o", markersize=8, alpha=1.0, label="particle")

    # Finish decoration   
    ax.legend()

    while True:

        # Commands
        key = inp.read_key()

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

        # Limit velocities
        v = np.clip(v, -vmax, vmax)
        w = np.clip(w, -wmax, wmax)

        # Digital odometric localization
        x = x + v*dt*np.cos(theta)
        y = y + v*dt*np.sin(theta)
        theta = theta + w*dt

        # Limit pose
        x = np.clip(x, 0.98*xmin, 0.98*xmax)
        y = np.clip(y, 0.98*ymin, 0.98*ymax)
        tetha = wrap_angle(theta)

        # Update particle
        particle.set_data([x], [y])

        # Update trail
        trail_x = np.append(trail_x, x)
        trail_y = np.append(trail_y, y)
        if len(trail_x) > trail_size:
            trail_x = trail_x[-trail_size:]
            trail_y = trail_y[-trail_size:]
        trail.set_data(trail_x, trail_y)

        # Upate 
        fig.supxlabel(f'v: {v} w: {w}')

        # Update graphics
        plt.pause(0.00001)

    plt.ioff()
    plt.show()
    
    print("Bye!")

if __name__ == "__main__":
    main()
