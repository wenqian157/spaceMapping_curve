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

    def __eq__(self, other):
        return (abs(self.x) < .0001 and abs(other.x) < .0001) or (abs(self.y) < .0001 and abs(other.y) < .0001)

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

    def tan_2d(self):
        if abs(self.x) < .00001:
            return 10000
        else:
            return abs(self.y / self.x)

    def __getitem__(self, idx):
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        elif idx == 2:
            return self.z

    def to_tuple(self):
        return (self.x, self.y, self.z)

    def adjust_x(self, other):
        self.x = other.x

    def adjust_y(self, other):
        self.y = other.y

class QuadObj():
    sq2 = 2 ** .5
    
    # s_clean_set = {
    #     # cleaning set: odering : [(current node) int : 0 - nothing / 1 - x / 2 - y / 3 - both, (next node) int : 0 - nothing / 1 - x / 2 - y / 3 - both]
    #     'NN':[2, 0], 'NE':[1, 0], 'NS':[3,0], 'NW':[0,0],
    #     'EN':[1, 1], 'EE':[1, 2], 'ES':[3,0], 'EW':[0,0],
    #     'SN':[1, 1], 'SE':[1, 2], 'SS':[3,0], 'SW':[0,0],
    #     'WN':[1, 1], 'WE':[1, 2], 'WS':[3,0], 'WW':[0,0]
    # }
    
    # l_clean_set = {
    #     # cleaning set: odering : [(current node) int : 0 - nothing / 1 - x / 2 - y / 3 - both, (next node) int : 0 - nothing / 1 - x / 2 - y / 3 - both]
    #     'NN':[1, 1], 'NE':[1, 2], 'NS':[3,0], 'NW':[0,0],
    #     'EN':[1, 1], 'EE':[1, 2], 'ES':[3,0], 'EW':[0,0],
    #     'SN':[1, 1], 'SE':[1, 2], 'SS':[3,0], 'SW':[0,0],
    #     'WN':[1, 1], 'WE':[1, 2], 'WS':[3,0], 'WW':[0,0]
    # }

    def __init__(self, distance_function, c_pt=Vector(0,0), world_size = 100, quad_type="simple", max_levels=7, last_is_quad=False):
        self.world_size = world_size
        QuadNode.mx_d = max_levels
        QuadNode.lq = last_is_quad
        self.d_f = distance_function

        half_size = self.world_size * .5

        self.closed = False

        if quad_type == "simple":
            self.closed = True
            self.leafs = [QuadNode(c_pt, self.world_size * .5)]

        elif quad_type == "pair":
            self.closed = True
            self.leafs = [
                QuadNode(c_pt + Vector(0, half_size), self.world_size * .5, 'S'),
                QuadNode(c_pt + Vector(0, - half_size), self.world_size * .5, 'N')
            ]

        elif quad_type == "2/3":
            self.closed = True
            self.leafs = [
                QuadNode(c_pt + Vector(- half_size, 0.0), self.world_size * .5, 'W'),
                QuadNode(c_pt + Vector(- half_size, self.world_size), self.world_size * .5, 'S'),
                QuadNode(c_pt + Vector(half_size, self.world_size), self.world_size * .5, 'S'),
                QuadNode(c_pt + Vector(half_size, 0.0), self.world_size * .5, 'E'),
                QuadNode(c_pt + Vector(half_size, - self.world_size), self.world_size * .5, 'N'),
                QuadNode(c_pt + Vector(- half_size, - self.world_size), self.world_size * .5, 'N')
            ]

        elif quad_type == "3/4":
            self.closed = True
            l_v = Vector(-self.world_size, 0)
            r_v = Vector(self.world_size, 0)
            self.leafs = [
                QuadNode(c_pt + l_v + Vector(- half_size, 0.0), self.world_size * .5, 'W'),
                QuadNode(c_pt + l_v + Vector(- half_size, self.world_size), self.world_size * .5, 'S'),
                QuadNode(c_pt + l_v + Vector(half_size, self.world_size), self.world_size * .5, 'S'),
                QuadNode(c_pt + l_v + Vector(half_size, 0.0), self.world_size * .5, 'E'),
                QuadNode(c_pt + r_v + Vector(- half_size, 0.0), self.world_size * .5, 'W'),
                QuadNode(c_pt + r_v + Vector(- half_size, self.world_size), self.world_size * .5, 'S'),
                QuadNode(c_pt + r_v + Vector(half_size, self.world_size), self.world_size * .5, 'S'),
                QuadNode(c_pt + r_v + Vector(half_size, 0.0), self.world_size * .5, 'E'),
                QuadNode(c_pt + r_v + Vector(half_size, - self.world_size), self.world_size * .5, 'N'),
                QuadNode(c_pt + r_v + Vector(- half_size, - self.world_size), self.world_size * .5, 'N'),
                QuadNode(c_pt + l_v + Vector(half_size, - self.world_size), self.world_size * .5, 'N'),
                QuadNode(c_pt + l_v + Vector(- half_size, - self.world_size), self.world_size * .5, 'N')
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

        if self.closed:
            return pt_list + [pt_list[0]]
        else:
            return pt_list

    def tuple_list(self):
        return [v.to_tuple() for v in self.pt_list()]

    def adjusting(self):

        should_run = True
        while (should_run):
            should_run = False
            for i in range(0, len(self.nodes), 1):
                made_change = self.clean_node(i)
                if made_change:
                    should_run = False

    def clean_node(self, i):
        d_0, d_1 = self.nodes[i].d, self.nodes[(i + 1)%len(self.nodes)].d
        # if d_0 == d_1:
        #     return False
        # else:
        t_val = (self.nodes[i].o - self.nodes[(i + 1)%len(self.nodes)].o).tan_2d()

        if abs(t_val) < 1000 or abs(t_val) > .0001:
            if d_0 < d_1:
                self.nodes[i].adjust_simple(self.nodes[(i + 1)%len(self.nodes)])
                return True
            elif d_0 > d_1:
                self.nodes[(i + 1)%len(self.nodes)].adjust_simple(self.nodes[i])
                return True
            else:
                # self.nodes[(i + 1)%len(self.nodes)].adjust_simple(self.nodes[i])
                return False

        else:
            return False


    def orientation_list(self):
        return [node.dir for node in self.nodes]

    def __repr__(self):
        try:
            str_list=["Hilbert Quad Object with {} items:".format(len(self.nodes))]
            for node in self.nodes:
                str_list.append("\t{}".format(str(node)))
            
            return '\n'.join(str_list)
        
        except:
            return "Hilbert Quad Object with for which the nodes haven't been initialized yet"

    def get_boundaries(self):
        return [node.get_boundary() for node in self.nodes]

class QuadNode():
    mx_d = 8
    lq = False
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
        if distance_function.get_distance(self.o) - self.d - QuadNode.lq> 0.0 and self.d + QuadNode.lq < QuadNode.mx_d:
            return self.__divide(d_f=distance_function)
        else:
            if QuadNode.lq > 0:
                return self.__force_divide(QuadNode.lq)

            else:
                return [self]

    def __force_divide(self, lvls=1):
        
        if lvls > 0:
            node_list = []

            half_l = .5 * self.l

            shift_vals = [- half_l, half_l]

            for location, direction in QuadNode.hilbert_map[self.dir]:
                move_vec = Vector(shift_vals[location[0]], shift_vals[location[1]])
                loc_node = QuadNode(self.o + move_vec, half_l, direction, self.d + 1)

                node_list.extend(loc_node.__force_divide(lvls-1))

            return node_list

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

    def adjust_simple(self, other):
        tangent_val = (other.o - self.o).tan_2d()

        if tangent_val > 1:
            self.adjust_x(other)
        
        else:
            self.adjust_y(other)

    def get_boundary(self):
        return [
            self.o + Vector(self.l, self.l),
            self.o + Vector(self.l, - self.l),
            self.o + Vector(- self.l, - self.l),
            self.o + Vector(- self.l, self.l)
        ]

    def adjust_x(self, other):
        # self.d = other.d
        self.o.adjust_x(other.o)

    def adjust_y(self, other):
        # self.d = other.d
        self.o.adjust_y(other.o)

    def adjust_both(self, other):
        # self.d = other.d
        self.adjust_x(other)
        self.adjust_y(other)

    def __str__(self):
        return "Node with depth {}, direction {} and {}".format(self.d, self.dir, self.o)

    def __repr__(self):
        return str(self)