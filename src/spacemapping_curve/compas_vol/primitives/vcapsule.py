from compas.geometry import Point
from compas.geometry._core import closest_point_on_segment
from compas import PRECISION

__all__ = ['VolCapsule']


class VolCapsule(object):
    """A volumetric capsule is defined by a line segment and a radius.

    Parameters
    ----------
    segment: list or tuple of two points
        Start and end point of the line segment.
    radius: float
        The radius of the capsule.

    Examples
    --------
    >>> sp = (1, 2, -3)
    >>> ep = (5, 4, 3)
    >>> segment = (sp, ep)
    >>> capsule = VolCapsule(segment, 3.0)
    """
    def __init__(self, segment, radius):
        self.segment = segment
        self.radius = radius

    @property
    def data(self):
        return {'segment': self.segment,
                'radius': self.radius}

    def to_data(self):
        return self.data

    @data.setter
    def data(self, data):
        self.segment = data['segment']
        self.radius = data['radius']

    @classmethod
    def from_data(cls, data):
        segment = data['segment']
        radius = data['radius']
        vcapsule = cls(segment, radius)
        return vcapsule

    def __repr__(self):
        segment = 'hallo'
        return 'VolSegment({0},{1:.{2}f})'.format(segment, self.radius, PRECISION[:1])

    def get_distance(self, point):
        """
        single point distance function
        """
        if not isinstance(point, Point):
            point = Point(*point)
        p = closest_point_on_segment(point, self.segment)
        return point.distance_to_point(p) - self.radius

    def get_distance_numpy(self, x, y, z):
        """
        vectorized distance function
        """
        import numpy as np

        A = np.array([*self.segment[0]])
        B = np.array([*self.segment[1]])

        pnt_vecs = np.array([x - A[0], y - A[1], z - A[2]])
        line_vec = B - A
        line_len = np.sqrt(np.sum(line_vec**2))
        line_unitvec = line_vec/line_len
        pnt_vec_scaled = pnt_vecs * 1/line_len
        t = np.dot(line_unitvec, pnt_vec_scaled)
        t = np.where(t < 0, 0, t)
        t = np.where(t > 1, 1, t)
        nearest = t[:, :, :, np.newaxis] * line_vec
        ptmg = np.meshgrid(pnt_vecs[1], pnt_vecs[0], pnt_vecs[2])
        pts = np.stack((ptmg), axis=-1)
        dist = np.linalg.norm(nearest - pts, axis=-1)
        return dist - self.radius
        # return norm(cross(B-A, pnt-A), axis=-1)/norm(B-A) - self.radius


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    s = ((-9, -6, 0), (6, 9, 0))
    capsule = VolCapsule(s, 5.0)
    print(capsule)

    x, y, z = np.ogrid[-14:14:112j, -12:12:96j, -10:10:80j]

    m = capsule.get_distance_numpy(x, y, z)
    print(m.shape)
    plt.imshow(m[:, :, 25].T, cmap='RdBu')  # transpose because numpy indexing is 1)row 2) column instead of x y
    plt.colorbar()
    plt.axis('equal')
    plt.show()

    for y in range(-15, 15):
        s = ''
        for x in range(-30, 30):
            d = capsule.get_distance((x * 0.5, -y, 0))
            if d < 0:
                s += 'x'
            else:
                s += '.'
        print(s)
