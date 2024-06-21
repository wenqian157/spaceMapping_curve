# clean quadtree library
# using matplotlib and shapely

def distance_f(vec):

    return 5

class Vector():

    def __init__(self, x, y, z=0.0):
        if isinstance(x, tuple) or isinstance(x, list):
            if len(x) == 3:
                self.x, self.y, self.z = x[0], x[1], x[2]
            elif len(x) == 2:
                self.x, self.y, self.z = x[0], x[1], 0.0
            else:
                self.x, self.y, self.z = x[0], x[0], 0.0
        else:
            self.x = x
            self.y = y
            self.z = z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, val):
        return Vector(self.x * val, self.y * val, self.z * val)

    def __str__(self):
        return "Vector with coordinates: {}, {}".format(self.x, self.y)

    def __repr__(self):
        return str(self)

    def to_tuple(self):
        return (self.x, self.y, self.z)

class QuadObj():
    sq2 = 2 ** .5

    def __init__(self, distance_function, c_pt=Vector(0,0), world_size = 100, quad_type="simple", max_levels=5):
        self.world_size = world_size
        self.max_levels = max_levels
        self.d_f = distance_function

        half_size = self.world_size * .5

        if quad_type == "simple":
            self.leafs = [QuadNode(c_pt, self.world_size * .5)]

        elif quad_type == "pair":
            self.leafs = [
                QuadNode(c_pt + Vector(0, half_size), 'S'),
                QuadNode(c_pt + Vector(0, - half_size), 'N')
            ]

        elif quad_type == "2/3":
            self.leafs = [
                QuadNode(c_pt + Vector(- half_size, 0.0), 'W'),
                QuadNode(c_pt + Vector(- half_size, self.world_size), 'S'),
                QuadNode(c_pt + Vector(half_size, self.world_size), 'S'),
                QuadNode(c_pt + Vector(half_size, 0.0), 'E'),
                QuadNode(c_pt + Vector(half_size, - self.world_size), 'N'),
                QuadNode(c_pt + Vector(- half_size, - self.world_size), 'N')
            ]

        elif quad_type == "3/4":
            l_v = Vector(-self.world_size, 0)
            r_v = Vector(-self.world_size, 0)
            self.leafs = [
                QuadNode(c_pt + l_v + Vector(- half_size, 0.0), 'W'),
                QuadNode(c_pt + l_v + Vector(- half_size, self.world_size), 'S'),
                QuadNode(c_pt + l_v + Vector(half_size, self.world_size), 'S'),
                QuadNode(c_pt + l_v + Vector(half_size, 0.0), 'E'),
                QuadNode(c_pt + r_v + Vector(- half_size, 0.0), 'W'),
                QuadNode(c_pt + r_v + Vector(- half_size, self.world_size), 'S'),
                QuadNode(c_pt + r_v + Vector(half_size, self.world_size), 'S'),
                QuadNode(c_pt + r_v + Vector(half_size, 0.0), 'E'),
                QuadNode(c_pt + r_v + Vector(half_size, - self.world_size), 'N'),
                QuadNode(c_pt + r_v + Vector(- half_size, - self.world_size), 'N'),
                QuadNode(c_pt + l_v + Vector(half_size, - self.world_size), 'N'),
                QuadNode(c_pt + l_v + Vector(- half_size, - self.world_size), 'N')
            ]

    def create(self):
        self.nodes = []
        for leaf in self.leafs:
            self.nodes.extend(leaf.branch(self.d_f))

    def pt_list(self):
        try:
            pt_list = [node.o for node in self.nodes]
        except:
            self.create()
            pt_list = [node.o for node in self.nodes]

        return pt_list

    def tuple_list(self):
        return [v.to_tuple() for v in self.pt_list()]

    def __repr__(self):
        try:
            str_list=["Hilbert Quad Object with {} items:".format(len(self.nodes))]
            for node in self.nodes:
                str_list.append("\t{}".format(str(node)))
            
            return '\n'.join(str_list)
        
        except:
            return "Hilbert Quad Object with for which the nodes haven't been initialized yet"

class QuadNode():
    mx_d = 5
    hilbert_map = {
        'N': [((1, 1), 'E'), ((1, 0), 'N'), ((0, 0), 'N'), ((0, 1), 'W')],
        'E': [((1, 1), 'N'), ((0, 1), 'E'), ((0, 0), 'E'), ((1, 0), 'S')],
        'S': [((0, 0), 'W'), ((0, 1), 'S'), ((1, 1), 'S'), ((1, 0), 'E')],
        'W': [((0, 0), 'S'), ((1, 0), 'W'), ((1, 1), 'W'), ((0, 1), 'N')]
    }

    def __init__(self, pt=Vector(0,0), side_l=100, direction='N', depth=0):
        self.o = pt
        self.l = side_l
        self.dir = direction
        self.d = depth

    def branch(self, distance_function):
        if distance_function(self.o) - self.d > 0.0 and self.d < QuadNode.mx_d:
            return self.__divide(d_f=distance_function)
        else:
            return [self]

    def __divide(self, d_f):
        node_list = []

        half_l = .5 * self.l

        shift_vals = [- half_l, half_l]

        for location, direction in QuadNode.hilbert_map[self.dir]:
            move_vec = Vector(shift_vals[location[0]], shift_vals[location[1]])
            loc_node = QuadNode(self.o + move_vec, half_l, direction, self.d + 1)

            node_list.extend(loc_node.branch(d_f))

        return node_list

    def __str__(self):
        return "Node with depth {}, direction {} and {}".format(self.d, self.dir, self.o)

    def __repr__(self):
        return str(self)