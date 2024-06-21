from quadtree import *
import rhinoscriptsyntax as rs

def draw_hc(ws, ml, function, return_pts = False):
    tree = Quadtree()
    tree._ws = ws
    tree._ml = ml
    tree._o = function
    tree._rn = QuadNode(0, 0, 0, ws, 0, 1)
    tree.divide(tree._rn)
    pts = []

    for node in tree.leafs:
        pt = node._p
        pts.append(pt)
    
    if not(return_pts):
        pl = rs.AddPolyline(pts)

    else:
        pl = pts

    return pl

def draw_hc_b(ws, ml, function, return_pts = False, q_node=None):
    tree = QuadtreeB()
    tree._ws = ws
    tree._ml = ml
    tree._o = function
    if q_node == None:
        # tree._rn = QuadNode(0, 0, 50, ws, 0, 1)
        tree.leafs = [QuadNode(0, 0, 0, ws, 0, 0)]
    elif q_node == "double":
        tree.leafs = [QuadNode(0, ws * .5, 0, ws, 0, 0), QuadNode(0, ws * -.5, 0, ws, 0, 0)]
    elif q_node == "sextant":
        tree.leafs = [QuadNode(0, ws * .5, 0, ws, 0, 0), QuadNode(0, ws * -.5, 0, ws, 0, 0)]
    # tree.divide(tree._rn)
    pts_all = []

    for node in tree.leafs:
        pts = [b._p for b in node._branches]    
        pts_all.extend(pts)
    
    if not(return_pts):
        pl = rs.AddPolyline(pts_all)

    else:
        pl = pts_all

    return pl

def draw_hc_b_multiple(ws, ml, function, return_pts = False, m_type = "single"):
    if m_type == "single":
        return draw_hc_b(ws, ml, function, return_pts)

    elif m_type == "double":
        return draw_hc_b(ws, ml, function, return_pts, q_node="double")

        