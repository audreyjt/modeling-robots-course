# Simulate a particle moving around a circle.
# Lawn mower robot
# https://youtu.be/2Rhsv8fFqCE

import numpy as np
import matplotlib.pyplot as plt

import eml4806.geometry.angle as angle

import eml4806.sensor.keyboard as keyboard

from eml4806.geometry.vector import vector
from eml4806.graphics.workspace import Workspace
from eml4806.graphics.shape import Rectangle, Circle, Polyline, Group, Arrow
from eml4806.graphics.style import Color, Style
from eml4806.geometry.transform import Transform
from eml4806.robot.odometry import AnalyticalSkidDriveOdometer
from eml4806.robot.skidsteer import Chassis, Wheel, Motor, Blade, Robot


def plot_path(points, ptype="line"):
    plt.plot(points[0], points[1], c='k')
    return None


def find_closest_point_on_segment(x1, y1, x2, y2, px, py):
    """
    Finds the point on the line segment P1(x1, y1) to P2(x2, y2)
    that is closest to the given point P(px, py).

    Args:
        x1, y1 (float): Coordinates of the segment's start point (P1).
        x2, y2 (float): Coordinates of the segment's end point (P2).
        px, py (float): Coordinates of the reference point (P).

    Returns:
        tuple: (closest_x, closest_y) coordinates on the segment.
    """
    # 1. Define the vectors and points
    P1 = np.array([x1, y1])
    P2 = np.array([x2, y2])
    P = np.array([px, py])

    # Vector P1 to P2 (v)
    v = P2 - P1

    # Vector P1 to P (w)
    w = P - P1

    # Square of the segment length (v dot v)
    v_sq = np.dot(v, v)

    # Handle the edge case where the two points are the same
    if v_sq == 0:
        return x1, y1

    # 2. Calculate projection parameter 't'
    # t = (w dot v) / (v dot v)
    # This determines where the projection of P falls on the line defined by P1 and P2.
    t = np.dot(w, v) / v_sq

    # 3. Clamp 't' to the range [0, 1] for the line *segment*
    # t_clamped = 0: Closest point is P1
    # t_clamped = 1: Closest point is P2
    # 0 < t_clamped < 1: Closest point is between P1 and P2
    t_clamped = np.clip(t, 0.0, 1.0)

    # 4. Find the closest point (P_closest)
    # P_closest = P1 + t_clamped * v
    P_closest = P1 + t_clamped * v

    return P_closest[0], P_closest[1]

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
    robot.setDebug(False)

    # Direct wheel-speed control modeling a microcontroller-style PWM motor driver
    # v = omega*r_wheel
    vl = 0.0  # Left track linear velocity (m/s)
    vr = 0.0  # Left track linear velocity (m/s)
    vmax = motors.maximum_angular_velocity * (0.5* wheels.diameter)

    # Controller sensitivity
    dv = 0.07  # m/s, Linear velocity increase
    dw = 0.04  # m/s, Angular velocity increse 

    # Simulation
    t = 0.0 # s
    dt = 0.1 # s (~50 Hz)

    line_pts = [[1, 8], [2, 9]]
    plot_path(line_pts)

    closest_p = find_closest_point_on_segment(x1=line_pts[0][0], x2=line_pts[0][1], y1=line_pts[1][0],
                                              y2=line_pts[1][1], px=x0, py=y0)
    plotted_closest = plt.scatter(closest_p[0], closest_p[1])
    robot.setDebug(True)
    last_error = [0,0]
    stored_errors = []

    while True:

        # User controller
        key = keyboard.key()

        # Commands inside the microntroller
        if key == "q":
            break
        elif key == "up":
            vl += dv
            vr += dv
        elif key == "down":
            vl -= dv
            vr -= dv
        elif key == "left":
            vl -= dw
            vr += dw
        elif key == "right":
            vl += dw
            vr -= dw
        elif key == " ":
            vl = 0.0
            vr = 0.0
        elif key == "d":
            robot.setDebug( not robot.debug() )
          
        # Motors physical limits
        vl = np.clip(vl, -vmax, vmax)
        vr = np.clip(vr, -vmax, vmax)

        ###################################################################################
        # Controller

        # Sensor
        x, y = robot.gps()

        # Controller
        # ...
        closest_p = find_closest_point_on_segment(x1=line_pts[0][0], x2=line_pts[0][1], y1=line_pts[1][0],
                                                  y2=line_pts[1][1], px=x, py=y)
        plotted_closest.set_offsets(np.c_[closest_p[0], closest_p[1]])

        cur_error = closest_p-np.array([x,y])
        norm_error = np.linalg.norm(cur_error)
        stored_errors.append(norm_error)
        plt.title(f"Error = {norm_error}")

        v = 0.2
        k_p = 0.0225
        k_d = 0.09

        dt_diff = (cur_error - last_error)/dt
        vl = v + k_p*cur_error[0] + k_d*dt_diff[0]
        vr = v + k_p*cur_error[1] + k_d*dt_diff[1]

        last_error = cur_error

        # Actuator
        robot.move(vl, vr, dt)  # Actuator
        # Advance
        t += dt

        ###################################################################################

        # Update scene
        workspace.update()

    
    print("Bye!")
    return k_p, k_d, stored_errors

if __name__ == "__main__":
    kp, kd, se = main()
    plt.clf()
    plt.plot(se)
    plt.title(f"Model Performance: Error vs Time | k_p={kp}, k_d={kd}")
    plt.grid(True)
    plt.show()