import numpy as np

def make(x, y):
    return np.array([0.0, 0.0], dtype=float)

def null():
    return np.array([0.0, 0.0], dtype=float)

def length(v1):
    v = np.asarray(v1)
    return np.linalg.norm(v) # np.sqrt(v[0]**2 + v[1]**2)

def coincident(v1, v2, tol=1e-2):
    v1 = np.asarray(v1)
    v2 = np.asarray(v2)
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
        return make(v[1], -v[0])
    else:
        make(-v[1], v[0])

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

def ensure(points):
    """
    Convert any 2-D vector input into a NumPy array of shape (N, 2).
    If points is None or empty, return an empty (0, 2) array.
    """
    if points is None or len(points) == 0:
        return np.zeros((0, 2), dtype=float)

    arr = np.asarray(points)

    # Already correct shape (N, 2)
    if arr.ndim == 2 and arr.shape[1] == 2:
        return arr

    # Shape (2, N) → treat as [x[], y[]]
    if arr.ndim == 2 and arr.shape[0] == 2:
        return np.column_stack(arr)

    # Flat → reshape into pairs
    if arr.ndim == 1:
        if arr.size % 2 != 0:
            raise ValueError("Flat sequence must have even length to form vectors.")
        return arr.reshape(-1, 2)

    # List of arbitrary sequences → pull first two components
    try:
        x = np.asarray([p[0] for p in points])
        y = np.asarray([p[1] for p in points])
        return np.column_stack((x, y))
    except:
        raise ValueError("Input cannot be interpreted as a sequence of 2D vectors.")

def append(points, new_points):
    """
    Append one or more 2D vectors to an existing point array.
    Uses ensure_points_2d() so both inputs are normalized to (N,2).
    """
    p = ensure(points)
    q = ensure(new_points)

    return np.vstack([p, q])
