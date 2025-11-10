import numpy as np

def normalize(radians):
    return np.mod(radians, 2*np.pi)