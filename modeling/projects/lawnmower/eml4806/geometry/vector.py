import numpy as np

def vector(x, y):
    return np.array([0.0, 0.0], dtype=float)

def null():
    return np.array([0.0, 0.0], dtype=float)

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

def perpendicular(v, clockwise=False, normalize=False):
    u = np.asarray(v)
    if clockwise:
        return vector(v[1], -v[0])
    else:
        vector(-v[1], v[0])

def combine(x, y):
    if np.isscalar(x) and np.isscalar(y):
        return np.array([x, y], dtype=float)
    return np.column_stack((np.asarray(x), np.asarray(y)))

def split(v):
    v = np.asarray(v)
    if v.ndim == 1:
        if v.size != 2:
            raise ValueError("1D input must have exactly 2 elements for x and y.")
        return float(v[0]), float(v[1])
    if v.ndim == 2 and v.shape[1] == 2:
        return v[:, 0], v[:, 1]
    raise ValueError("Input must be shape (2,) or (N, 2).")
