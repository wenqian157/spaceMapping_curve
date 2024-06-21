import math
import Rhino.Geometry as rg

class TPMS:

    X_SCALE = 5.0
    Y_SCALE = 5.0
    Z_SCALE = 5.0

    HEIGHT = 20.0

    GLOBAL_SCALE = 40.0

    def __init__(self, x_scale = 1.0, y_scale = 1.0, z_scale = 1.0, height = 0.0, global_scale = 1.0):

        if x_scale == None:
            self.x_scale = TPMS.X_SCALE

        else:
            self.x_scale = x_scale

        if y_scale == None:
            self.y_scale = TPMS.Y_SCALE

        else:
            self.y_scale = y_scale

        if z_scale == None:
            self.z_scale = TPMS.Z_SCALE

        else:
            self.z_scale = z_scale

        if height == None:
            self.height_scale = TPMS.HEIGHT

        else:
            self.height = height

        if global_scale == None:

            self.global_scale = TPMS.GLOBAL_SCALE

        else:
            self.global_scale = global_scale

    def xyz_scale(self, pt):
        x_val = pt[0] / self.x_scale
        y_val = pt[1] / self.y_scale
        z_val = (pt[2] - self.height) / self.z_scale

        return x_val, y_val, z_val

    def try_domain_range(self, count = 20, scale = .1):
        angle_list = [i * scale * math.pi for i in range(count)]

        values = []

        for x in angle_list:
            for y in angle_list:
                for z in angle_list:

                    values.append(self.get_distance((x, y, z)))

        return min(values), max(values)

    @property
    def domain(self):

        return self.try_domain_range()

# class HelicoidCatenoid(TPMS):
class HelicoidCatenoid:

    X_SCALE = 5.0
    Y_SCALE = 5.0
    Z_SCALE = 5.0

    HEIGHT = 20.0

    GLOBAL_SCALE = 40.0

    RHO = 1.0
    ALFA = 2.0

    def __init__(self, x_scale = None, y_scale = None, z_scale = None, height = None, global_scale = None, rho = None, alfa = None):
        # super().__init__(x_scale, y_scale, z_scale, height, global_scale)

        if x_scale == None:
            self.x_scale = TPMS.X_SCALE
        else:
            self.x_scale = x_scale

        if y_scale == None:
            self.y_scale = TPMS.Y_SCALE
        else:
            self.y_scale = y_scale

        if z_scale == None:
            self.z_scale = TPMS.Z_SCALE
        else:
            self.z_scale = z_scale

        if height == None:
            self.height_scale = TPMS.HEIGHT
        else:
            self.height = height

        if global_scale == None:
            self.global_scale = TPMS.GLOBAL_SCALE
        else:
            self.global_scale = global_scale

        if rho == None:
            self.rho = HelicoidCatenoid.RHO
        else:
            self.rho = rho

        if alfa == None:
            self.alfa = HelicoidCatenoid.ALFA
        else:
            self.alfa = alfa

    def xyz_scale(self, pt):

        x_val = pt[0] / self.x_scale
        y_val = pt[1] / self.y_scale
        z_val = (pt[2] - self.height) / self.z_scale

        return x_val, y_val, z_val

# class PinchShapes(TPMS):
class PinchShapes:

    X_SCALE = 5.0
    Y_SCALE = 5.0
    Z_SCALE = 5.0

    HEIGHT = 20.0

    GLOBAL_SCALE = 40.0

    R = 10.0
    S = -.5
    T = -14.0

    def __init__(self, x_scale = 1.0, y_scale = 1.0, z_scale = 1.0, height = 0.0, global_scale = 1.0, r = None, s = None, t = None):

        # super(PinchShapes, self).__init__(x_scale, y_scale, z_scale, height, global_scale)
        # super(PinchShapes, self).__new__(x_scale, y_scale, z_scale, height, global_scale)

        ###
        if x_scale == None:
            self.x_scale = TPMS.X_SCALE
        else:
            self.x_scale = x_scale

        if y_scale == None:
            self.y_scale = TPMS.Y_SCALE
        else:
            self.y_scale = y_scale

        if z_scale == None:
            self.z_scale = TPMS.Z_SCALE
        else:
            self.z_scale = z_scale

        if height == None:
            self.height_scale = TPMS.HEIGHT
        else:
            self.height = height

        if global_scale == None:
            self.global_scale = TPMS.GLOBAL_SCALE
        else:
            self.global_scale = global_scale

        ###

        if r == None:
            self.r = PinchShapes.R
        else:
            self.r = r

        if s == None:
            self.s = PinchShapes.S
        else:
            self.s = s

        if t == None:
            self.t = PinchShapes.T
        else:
            self.t = t

    def xyz_scale(self, pt):

        x_val = pt[0] / self.x_scale
        y_val = pt[1] / self.y_scale
        z_val = (pt[2] - self.height) / self.z_scale

        return x_val, y_val, z_val

    def try_domain_range(self):

        angle_list = [i * .1 * math.pi for i in range(20)]

        values = []

        for x in angle_list:
            for y in angle_list:
                for z in angle_list:

                    values.append(self.get_distance((x, y, z)))

        return min(values), max(values)

    @property
    def domain(self):

        return self.try_domain_range()

class SchwarzG(TPMS):

    def get_distance(self, pt):

        x, y, z = self.xyz_scale(pt)

        dis = math.cos(x) + math.cos(y) + math.cos(z)

        return dis * self.global_scale

class Gyroid(SchwarzG):

    pass

class SchwarzP(TPMS):

    def get_distance(self, pt):

        x, y, z = self.xyz_scale(pt)

        dis = math.sin(z)*math.cos(y)+math.sin(y)*math.cos(x)+math.sin(z)*math.cos(x)

        return dis * self.global_scale

class SchwarzD(TPMS):

    def get_distance(self, pt):

        x, y, z = self.xyz_scale(pt)

        s_x, s_y, s_z = math.sin(x), math.sin(y), math.sin(z)
        c_x, c_y, c_z = math.cos(x), math.cos(y), math.cos(z)

        dis = s_x * s_y * s_z + s_x * c_y * c_z + c_x * s_y * c_z + c_x * c_y * s_z

        return dis * self.global_scale

class SchwarzN(TPMS):

    def get_distance(self, pt):

        x, y, z = self.xyz_scale(pt)
        c_x, c_y, c_z = math.cos(x), math.cos(y), math.cos(z)

        dis = 3 * (c_x + c_y + c_z) + 4 * (c_x * c_y * c_z)

        return dis * self.global_scale

class Neovius(SchwarzN):

    pass

class Lindinoid(TPMS):

    def get_distance(self, pt):

        x, y, z = self.xyz_scale(pt)

        c_x, c_y, c_z = math.cos(x), math.cos(y), math.cos(z)
        c_2x, c_2y, c_2z = math.cos(2 * x), math.cos(2 * y), math.cos(2 * z)
        s_x, s_y, s_z = math.sin(x), math.sin(y), math.sin(z)
        s_2x, s_2y, s_2z = math.sin(2 * x), math.sin(2 * y), math.sin(2 * z)

        term_a = s_2x * c_y * s_z + s_2y * c_z * s_x + s_2z * c_x * s_y
        term_b = c_2x * c_2y + c_2y * c_2z + c_2z * c_2x

        dis = term_a * .5 - term_b * .5 + .15

        return dis * self.global_scale

class SchwarzW(TPMS):

    def get_distance(self, pt):

        x, y, z = self.xyz_scale(pt)

        c_x, c_y, c_z = math.cos(x), math.cos(y), math.cos(z)

        dis = c_x * c_y + c_y * c_z + c_z * c_x - c_x * c_y * c_z

        return dis * self.global_scale 

class iWP(SchwarzW):

    pass

class SchwarzPW(TPMS):

    def get_distance(self, pt):

        x, y, z = self.xyz_scale(pt)

        c_x, c_y, c_z = math.cos(x), math.cos(y), math.cos(z)

        dis = 4 * (c_x * c_y + c_y * c_z + c_z * c_x) - 3 * c_x * c_y * c_z + 2.4

        return dis * self.global_scale

class PWHybrid(SchwarzPW):

    pass

class PinchG(PinchShapes):

    def get_distance(self, pt):

        x, y, z = self.xyz_scale(pt)

        c_x, c_y, c_z = math.cos(x), math.cos(y), math.cos(z)
        c_2x, c_2y, c_2z = math.cos(2 * x), math.cos(2 * y), math.cos(2 * z)

        t1 = c_x*c_y + c_y*c_z + c_z*c_x
        t2 = c_2x + c_2y + c_2z

        dis = t1 * self.r + t2 * self.s + self.t

        return dis * self.global_scale

class PinchD(PinchShapes):

    def get_distance(self, pt):

        x, y, z = self.xyz_scale(pt)

        s_x0, s_y0, s_z0 = math.sin(x - 0.78539816), math.sin(y - 0.78539816), math.sin(z - 0.78539816)
        c_x0, c_y0, c_z0 = math.cos(x - 0.78539816), math.cos(y - 0.78539816), math.cos(z - 0.78539816)
        c_4x, c_4y, c_4z = math.cos(4 * x), math.cos(4 * y), math.cos(4 * z)

        t1 = s_x0 * s_y0 * s_z0 + s_x0 * c_y0 * c_z0 + c_x0 * s_y0 * c_z0 + c_x0 * c_y0 * s_z0
        t2 = c_4x + c_4y + c_4z

        dis = t1 * self.r + t2 * self.s + self.t

        return dis * self.global_scale

class PinchP(PinchShapes):

    def get_distance(self, pt):

        x, y, z = self.xyz_scale(pt)

        s_x, s_y, s_z = math.sin(x), math.sin(y), math.sin(z)
        c_x, c_y, c_z = math.cos(x), math.cos(y), math.cos(z)
        c_2x, c_2y, c_2z = math.cos(2 * x), math.cos(2 * y), math.cos(2 * z)

        t1 = c_x * s_y + c_y * s_z + c_z * s_x
        t2 = c_2x * c_2y + c_2y * c_2z + c_2z * c_2x

        dis = t1 * self.r + t2 * self.s + self.t

        return dis * self.global_scale

class PinchW(PinchShapes):

    def get_distance(self, pt):

        x, y, z = self.xyz_scale(pt)

        c_x, c_y, c_z = math.cos(x), math.cos(y), math.cos(z)

        t1 = c_x + c_y + c_z
        t2 = c_x * c_y + c_y * c_z + c_z * c_x

        dis = t1 * self.r + t2 * self.s + self.t

        return dis * self.global_scale

class Helicoid(HelicoidCatenoid):

    def get_distance(self, pt):

        x, y, z = self.xyz_scale(pt)

class DistanceToCurve:

    GLOBAL_SCALE = 8.0

    def __init__(self, crvs):

        if not(isinstance(crvs, list)):

            self.crvs = [crvs]

        else:

            self.crvs = crvs

    def get_distance(self, pt):
        
        other_pt = rg.Point3d(pt[0], pt[1], pt[2])

        distance_list = []

        for crv in self.crvs:

            pt_on_crv = crv.PointAt(crv.ClosestPoint(other_pt)[1])

            distance = pt_on_crv.DistanceTo(other_pt) / DistanceToCurve.GLOBAL_SCALE

            distance_list.append(distance)

        distance_list.sort()

        return distance_list[0]