import numpy as np

#########################################################

class Transform:

    def __init__(self, position=(0.0, 0.0), orientation=0.0, scaling=(1.0, 1.0)):
        self.position = np.asarray(position, dtype=float).reshape(2)
        self.orientation = float(orientation)
        self.scaling = np.asarray(scaling, dtype=float).reshape(2)

    @property
    def matrix(self):
        return Transform.to_matrix(self)

    @property
    def inverse(self):
        return np.linalg.inv(self.matrix)

    def clone(self):
        return Transform(self.position.copy(), self.orientation, self.scaling.copy())

    def translate(self, dx, dy):
        self.position += np.array([dx, dy], dtype=float)

    def rotate(self, da):
        self.orientation += float(da)

    def scale(self, sx, sy=None):
        if sy is None:
            sy = sx
        self.scaling *= np.array([sx, sy], dtype=float)

    def apply(self, points, inverse=False):
        pts = np.asarray(points, dtype=float)
        p = pts.reshape(-1, 2)  # (N, 2)
        # Extract transform components
        tx, ty = self.position
        rot = self.orientation
        sx, sy = self.scaling
        if not inverse:
            # Scale
            x = p[:, 0] * sx
            y = p[:, 1] * sy
            # Rotate
            c = np.cos(rot)
            s = np.sin(rot)
            out_x = c * x - s * y
            out_y = s * x + c * y
            # Translate
            out_x += tx
            out_y += ty
        else:
            # Un-translate
            x = p[:, 0] - tx
            y = p[:, 1] - ty
            # Un-rotate
            c = np.cos(rot)
            s = np.sin(rot)
            out_x = c * x + s * y
            out_y = -s * x + c * y
            # Un-scale
            out_x /= sx
            out_y /= sy
        out = np.column_stack((out_x, out_y))
        if pts.ndim == 1:
            return out[0]
        return out.reshape(pts.shape)

    @classmethod
    def compound(cls, M1, M2):
        M = M1.matrix @ M2.matrix
        return Transform.from_matrix(M)

    @classmethod
    def identity(cls):
        return cls()

    @classmethod
    def translation(cls, x, y):
        return cls((x, y), 0.0, (1.0, 1.0))

    @classmethod
    def rotation(cls, angle):
        return cls((0.0, 0.0), angle, (1.0, 1.0))

    @classmethod
    def scale(cls, sx, sy=None):
        if sy is None:
            sy = sx
        return cls((0.0, 0.0), 0.0, (sx, sy))

    @classmethod
    def from_matrix(cls, M):
        M = np.asarray(M, dtype=float)
        assert M.shape == (3, 3), "Matrix must be 3x3"
        # Translation
        tx, ty = M[0, 2], M[1, 2]
        # Upper-left 2x2 contains rotation * scale
        a, b = M[0, 0], M[0, 1]
        c, d = M[1, 0], M[1, 1]
        # Scale is length of the column vectors
        sx = np.sqrt(a * a + c * c)
        sy = np.sqrt(b * b + d * d)
        # Rotation is angle of first column
        rot = np.arctan2(c, a)
        return cls((tx, ty), rot, (sx, sy))

    @classmethod
    def to_matrix(cls, tf):
        tx, ty = tf.position
        c = np.cos(tf.orientation)
        s = np.sin(tf.orientation)
        sx, sy = tf.scaling
        return np.array(
            [[c * sx, -s * sy,  tx],
             [s * sx,  c * sy,  ty], 
             [   0.0,     0.0, 1.0]], dtype=float
        )
