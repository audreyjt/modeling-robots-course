from abc import ABC, abstractmethod
from dataclasses import dataclass
from numpy import pi, sin, cos, clip
from eml4806.geometry.angle import normalize

##############################################################################################

@dataclass
class SkidDriveOdometer(ABC):
    track_width             : float = 0.0 # Effective_track_width # Distance between the left and right wheel contact lines
    maximum_linear_velocity : float = None # Impose safety speed limites in the internal controller
    maximum_angular_velocity: float = None # Impose safety rotation limites in the internal controller
    
    def initilize(self, x, y, theta):
        self._x = x
        self._y = y
        self._theta = theta
        self._vl = 0.0
        self._vr = 0.0

    def position(self):
        return self._x, self._y
    
    def orientation(self):
        return self._theta
    
    def pose(self):
        return self._x, self._y, self._theta
    
    def velocities(self):
        return self._vr, self._vl

    def integrate(self, vl, vr, dt, tol=1e-3):
        # Remember
        self._vl = vl
        self._vr = vr
        # Forward and angular velocities
        v = 0.5 * (vr + vl)  # forward
        w = (vr - vl) / self.track_width  # yaw rate
        # Imposed safety limits
        v = clip(v, -self.maximum_linear_velocity, self.maximum_linear_velocity)
        w = clip(w, -self.maximum_angular_velocity, self.maximum_angular_velocity)
        # Update pose
        self._integrate(v, w, dt, tol)

    @abstractmethod
    def _integrate(self, v, w, dt, tol): ...

##############################################################################################

@dataclass
class FirstOrderSkidDriveOdometer(SkidDriveOdometer):
    
    def _integrate(self, v, w, dt, tol):
        ds = v*dt # Forward linear displacement
        da = w*dt # Change in heading (yaw)
        self._x += ds*cos(self._theta)
        self._y += ds*sin(self._theta)
        self._theta += da

##############################################################################################

@dataclass
class SecondOrderSkidDriveOdometer(SkidDriveOdometer):
    
    def _integrate(self, v, w, dt, tol):
        ds = v*dt # Forward linear displacement
        da = w*dt # Change in heading (yaw)
        a = self._theta + 0.5*da # Midpoint heading
        self._x += ds * cos(a)
        self._y += ds * sin(a)
        self._theta += da
        
##############################################################################################

@dataclass
class AnalyticalSkidDriveOdometer(SkidDriveOdometer):
        
    def _integrate(self, v, w, dt, tol):
        ds = v*dt # Forward linear displacement
        da = w*dt # Change in heading (yaw)
        # Straigth line (small-angle) case 
        if abs(da) < tol:
            a = self._theta + 0.5*da # Midpoint heading
            self._x += ds * cos(a)
            self._y += ds * sin(a)
            self._theta += da
        else:
            # General analytic case
            r = ds/da  # instantaneous turning radius
            a = self._theta + da # Heading
            self._x += r * (sin(a) - sin(self._theta))
            self._y -= r * (cos(a) - cos(self._theta))
            self._theta += da
