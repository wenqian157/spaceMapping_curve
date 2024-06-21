from math import sqrt
# from compas.geometry import Point

class Quadtree(object):
    sq2 = sqrt(2.0)
    sq3 = sqrt(3.0)

    def __init__(self):
        self._p = (0, 0, 0)
        self._ws = 100.0  # world size
        self._ml = 4      # max levels
        # self._rn = QuadNode(0, 0, 0, self._ws, 0, 1)
        self._o = None
        self.leafs = []
    
    def divide(self, node):
        d = self._o.get_distance(node._p)
        node.distance = d
        
        if node.level < self._ml:            
            if abs(d) < Quadtree.sq2 * node._el/2.0:
                node.divide_node()     
                for b in node._branches:
                    self.divide(b)
            else:
                self.leafs.append(node)
                    
        else:
            # if abs(node.distance) < Quadtree.sq2 * node._el/2.0:
            self.leafs.append(node)

class QuadtreeB(Quadtree):

    def divide(self, node):
        d = self._o.get_distance(node._p)
        node.distance = d
        
        if node.level < self._ml:            
            if abs(d) < Quadtree.sq2 * node._el/2.0:
                node.divide_node()     
                for b in node._branches:
                    self.divide(b)
            else:
                node.divide_node()
                self.leafs.append(node)
                    
        else:
            node.divide_node()
            self.leafs.append(node)

class QuadNode(object):
    def __init__(self, x, y, z, e, depth, orientation):
        self._p = (x, y, z)
        self._el = e
        self._l = depth
        if depth == 0:
            self.divide_node()
        self.distance = 0.0
        self.orientation = orientation
    
    @property
    def level(self):
        return self._l

    @level.setter
    def level(self, l):
        self._l = float(l)
    
    def divide_node(self):

        # direction based parameters

        base_list = [-1, -1, 1, 1]

        if self.orientation % 2 == 0:
            orientation_list = [1, 0, 0, -1]

        else:
            orientation_list = [-1, 0, 0, 1]

        self._branches = []
        res = self._el / 2.0
        half_res = res / 2.0

        new_depth = self.level + 1

        i_a, i_b = (1 - self.orientation)% 4, self.orientation

        # print(i_a, i_b)

        for i in range(4):

            self._branches.append(QuadNode(
                self._p[0] + base_list[(i + i_a) % 4] * half_res, 
                self._p[1] + base_list[(i + i_b) % 4] * half_res, 
                0, 
                res, 
                new_depth, 
                (self.orientation + orientation_list[i]) % 4
            ))

# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
