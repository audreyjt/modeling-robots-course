from abc import ABC, abstractmethod
from dataclasses import dataclass
from numpy import pi, sin, cos, clip
from eml4806.geometry.angle import normalize

##############################################################################################

@dataclass
class SkidDriveOdometer(ABC):
    track_width             : float = 0.0 # Effective_track_width # Distance between the left and right wheel contact lines
    maximum_linear_velocity : float = 0.0 # Impose safety speed limites in the internal controller
    maximum_angular_velocity: float = 0.0 # Impose safety rotation limites in the internal controller
    
    def initilize(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

    def integrate(self, vl, vr, dt, tol=1e-3):
        # Forward and angular velocities
        v = 0.5 * (vr + vl)  # forward
        w = (vr - vl) / self.track_width  # yaw rate
        # Imposed safety limits
        v = clip(v, -self.maximum_linear_velocity, self.maximum_linear_velocity)
        w = clip(w, -self.maximum_angular_velocity, self.maximum_angular_velocity)
        # Update pose
        self._integrate(v, w, dt, tol)
        return self.x, self.y, self.theta

    @abstractmethod
    def _integrate(self, v, w, dt, tol): ...

##############################################################################################

@dataclass
class FirstOrderSkidDriveOdometer(SkidDriveOdometer):
    
    def _integrate(self, v, w, dt, tol):
        ds = v*dt # Forward linear displacement
        da = w*dt # Change in heading (yaw)
        self.x += ds*cos(self.theta)
        self.y += ds*sin(self.theta)
        self.theta += da

##############################################################################################

@dataclass
class SecondOrderSkidDriveOdometer(SkidDriveOdometer):
    
    def _integrate(self, v, w, dt, tol):
        ds = v*dt # Forward linear displacement
        da = w*dt # Change in heading (yaw)
        a = self.theta + 0.5*da # Midpoint heading
        self.x += ds * cos(a)
        self.y += ds * sin(a)
        self.theta += da
        
##############################################################################################

@dataclass
class AnalyticalSkidDriveOdometer(SkidDriveOdometer):
        
    def _integrate(self, v, w, dt, tol):
        ds = v*dt # Forward linear displacement
        da = w*dt # Change in heading (yaw)
        # Straigth line (small-angle) case 
        if abs(da) < tol:
            a = self.theta + 0.5*da # Midpoint heading
            self.x += ds * cos(a)
            self.y += ds * sin(a)
            self.theta += da
        else:
            # General analytic case
            r = ds/da  # instantaneous turning radius
            a = self.theta + da # Heading
            self.x += r * (sin(a) - sin(self.theta))
            self.y -= r * (cos(a) - cos(self.theta))
            self.theta += da
