from dataclasses import dataclass
import numpy as np

from eml4806.geometry.vector import vector, coincident
from eml4806.geometry.transform import Transform
from eml4806.graphics.style import Color, Style, Stroke, Fill
from eml4806.graphics.shape import Rectangle, Circle, Polyline, Group, Vector

@dataclass
class Chassis:
    length    : float = 0.0 # m
    width     : float = 0.0 # m
    wheelbase : float = 0.0 # m
    trackwidth: float = 0.0 # m

@dataclass
class Wheel:
    diameter: float = 0.0  # m
    width: float = 0.0     # m

@dataclass
class Motor:
    maximum_angular_velocity: float = 0.0  # rad/s

@dataclass
class Blade:
    diameter : float = 0.0 # m
    on: bool = False
    height: float = 0.0 # m

class Robot:
    def __init__(self, workspace, x, y, theta, chassis, wheels, motors, blade, odometer):
        # Simulation
        self.t = 0.0 # s
        # Odometric pose
        self.x = x
        self.y = y
        self.theta = theta
        # Kinematics
        self.vl = 0.0
        self.vr = 0.0
        # Body
        self.chassis = chassis
        self.wheels = wheels
        self.motors = motors
        self.blade = blade
        # Odometry
        self.odemeter = odometer
        self.odemeter.initilize(x, y, theta)
        self._makeBody(workspace)
   
    def gps(self):
        return self.x, self.y

    # Control wheel shaft rotation (rad/s)
    def move(self, t, wl, wr):
        dt = t - self.t
        self.vl = wl*0.5*self.wheels.diameter
        self.vr = wr*0.5*self.wheels.diameter
        self.x, self.y, self.theta = self.odemeter.integrate(self.vl, self.vr, dt, tol=0.001)
        self.t = t
        self._update()

    def _clampWheelSpeeds(self, wl, wr):
        wl = np.clip(wl, -self.motors.maximum_angular_velocity, self.motors.maximum_angular_velocity)
        wr = np.clip(wr, -self.motors.maximum_angular_velocity, self.motors.maximum_angular_velocity)
        return wl, wr

    def _makeBody(self, workspace):
        # Parts
        c = self.chassis
        w = self.wheels
        b = self.blade
        self.body = Rectangle(workspace, 0.0, 0.0, c.length, c.width, style=Style.brush(Color(1.0,0.55,0.0), 0.5))
        self.wheel1 = Rectangle(workspace, -0.5*c.wheelbase, -0.5*c.trackwidth, w.diameter, w.width, style=Style.brush(Color(0.5,0.5,0.5), 0.5))
        self.wheel2 = Rectangle(workspace,  0.5*c.wheelbase, -0.5*c.trackwidth, w.diameter, w.width, style=Style.brush(Color(0.5,0.5,0.5), 0.5))
        self.wheel3 = Rectangle(workspace, -0.5*c.wheelbase,  0.5*c.trackwidth, w.diameter, w.width, style=Style.brush(Color(0.5,0.5,0.5), 0.5))
        self.wheel4 = Rectangle(workspace,  0.5*c.wheelbase,  0.5*c.trackwidth, w.diameter, w.width, style=Style.brush(Color(0.5,0.5,0.5), 0.5))
        self.tool = Circle(workspace, 0.0, 0.0, 0.5*b.diameter, style=Style.brush(Color(1.0,0.0,0.0), 0.5))
        # Debug
        self.vector_vl = Vector(workspace, 0.0, 0.5*c.trackwidth, 0.0, 0.0, style=Style.brush(Color(0.0,0.0,1.0), 0.5, 3.0), scale=1.25)
        self.vector_vr = Vector(workspace, 0.0,-0.5*c.trackwidth, 0.0, 0.0, style=Style.brush(Color(0.0,0.0,1.0), 0.5, 3.0), scale=1.25)
        # Assembly
        self.body = Group([self.body, self.wheel1, self.wheel2, self.wheel3, self.wheel4, self.tool, self.vector_vl, self.vector_vr])
        # Path
        self.path = Polyline(workspace, style=Style.pen(Color(0.0,0.0,1.0)))
        self.path.append(vector(self.x, self.y))
        self._update()

    def _update(self):
        self._updateBody()
        self._updatePath()
        self._updateDebug()

    def _updateBody(self):
        tf = Transform(position=(self.x, self.y), orientation=self.theta)
        self.body.setTransform(tf)
    
    def _updatePath(self):
        position = vector(self.x, self.y)
        last = self.path.last()
        if not coincident(position, last):
            self.path.append( position )

    def _updateDebug(self):
        self.vector_vl.setVector(self.vl, 0.0)
        self.vector_vr.setVector(self.vr, 0.0)