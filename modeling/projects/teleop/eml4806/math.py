import numpy as np

def null():
    return np.array([0.0, 0.0])

def length(v1):
    v = np.asarray(v1)
    return np.linalg.norm(v) # np.sqrt(v[0]**2 + v[1]**2)

def coincident(v1, v2, tol=1e-2):
    return np.allclose(v1, v2, atol=tol) # length(v1 - v2) <= tol

def unit(v1):
    v = np.asarray(v1)
    l = length(v)
    if l <= 0:
        return null()
    else:
        return v / l

def perpendicular(v1, clockwise=False, normalize=False):
    v = np.asarray(v1)
    if w.shape != (2,):
        raise ValueError("Input vector must be 2D (shape (2,))")
    if clockwise:
        return np.array([v[1], -v[0]])
    else:
        np.array([-v[1], v[0]])

def wrap_angle(theta):
    return np.mod(theta, 2*np.pi)