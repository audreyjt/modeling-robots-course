import math

def point_to_line_distance(x, y, x1, y1, x2, y2):
    """
    Returns the perpendicular distance from point (x, y)
    to the line defined by points (x1, y1) and (x2, y2).
    """
    # Line vector components
    A = x2 - x1
    B = y2 - y1

    # Cross product magnitude (2D)
    cross = abs(A * (y1 - y) - (x1 - x) * B)

    # Length of the line segment direction vector
    length = math.hypot(A, B)

    if length == 0:
        raise ValueError("The two points defining the line must not be identical.")

    return cross / length

def closest_point_on_line(xp, yp, x1, y1, x2, y2):
    """
    Returns the closest point (cx, cy) on the infinite line passing through
    (x1, y1) and (x2, y2) to the point (xp, yp).
    """

    # Line direction vector
    dx = x2 - x1
    dy = y2 - y1

    # Check for degenerate line
    if dx == 0 and dy == 0:
        raise ValueError("The two points defining the line must not be identical.")

    # Vector from line start to the point
    vx = xp - x1
    vy = yp - y1

    # Projection factor t of v onto line direction
    t = (vx * dx + vy * dy) / (dx * dx + dy * dy)

    # Closest point on the line
    cx = x1 + t * dx
    cy = y1 + t * dy

    return cx, cy