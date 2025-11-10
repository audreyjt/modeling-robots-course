import numpy as np

def to_homogeneous(vector):
    arr = np.asarray(vector, dtype=float)
    # Single vector
    if arr.ndim == 1:
        if arr.shape[0] != 2:
            raise ValueError("Expected a 2D vector of length 2.")
        return np.array([arr[0], arr[1], 1.0])
    # Multiple vectors
    elif arr.ndim == 2:
        if arr.shape[1] != 2:
            raise ValueError("Expected an array of shape (N, 2).")
        ones = np.ones((arr.shape[0], 1), dtype=float)
        return np.hstack([arr, ones])
    else:
        raise ValueError("Input must be a 1D or 2D array of 2D vectors.")

def from_homogeneous(hvector):
    arr = np.asarray(hvector, dtype=float)
    # Single vector
    if arr.ndim == 1:
        if arr.shape[0] != 3:
            raise ValueError("Expected a homogeneous vector of length 3.")
        w = arr[2]
        if w == 0:
            raise ValueError("Cannot convert homogeneous vector with w=0.")
        return arr[:2] / w
    # Multiple vectors
    elif arr.ndim == 2:
        if arr.shape[1] != 3:
            raise ValueError("Expected an array of shape (N, 3).")
        w = arr[:, 2:3]
        if np.any(w == 0):
            raise ValueError("Some vectors have w=0; cannot convert.")
        return arr[:, :2] / w
    else:
        raise ValueError("Input must be a 1D or 2D array of homogeneous 2D vectors.")

def identity():
    return np.eye(3, dtype=float)

def rotation(theta):
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, -s, 0.0],
                     [s,  c, 0.0],
                     [0.0, 0.0, 1.0]], dtype=float)

def translation(tx, ty):
    return np.array([[1.0, 0.0, tx],
                     [0.0, 1.0, ty],
                     [0.0, 0.0, 1.0]], dtype=float)

def scale(sx, sy=None):
    if sy is None:
        sy = sx
    return np.array([[sx, 0.0, 0.0],
                     [0.0, sy, 0.0],
                     [0.0, 0.0, 1.0]], dtype=float)

def mirror(axis='x'):
    axis = axis.lower()
    if axis == 'x':
        return np.array([[1.0, 0.0, 0.0],
                         [0.0, -1.0, 0.0],
                         [0.0, 0.0, 1.0]], dtype=float)
    elif axis == 'y':
        return np.array([[-1.0, 0.0, 0.0],
                         [ 0.0, 1.0, 0.0],
                         [ 0.0, 0.0, 1.0]], dtype=float)
    elif axis == 'origin':
        return np.array([[-1.0, 0.0, 0.0],
                         [ 0.0, -1.0, 0.0],
                         [ 0.0,  0.0, 1.0]], dtype=float)
    else:
        return identity()

def inverse(transform):
    return np.linalg.inv(transform)