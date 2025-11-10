
from dataclasses import dataclass
import numpy as np

@dataclass
class Pose:
    x: float = 0.0     # meters
    y: float = 0.0     # meters
    theta: float = 0.0 # radians (heading, CCW from +x)