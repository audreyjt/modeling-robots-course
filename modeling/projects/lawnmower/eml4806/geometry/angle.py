import numpy as np

# Normalize angle to the range [-pi, pi).
def normalize(radians):
    return (radians + np.pi) % (2 * np.pi) - np.pi