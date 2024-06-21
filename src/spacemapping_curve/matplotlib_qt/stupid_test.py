import sys

sys.path.append("/Users/jonas/Documents/reps/spacemapping_curve/src/spacemapping_curve/matplotlib_qt")

import quad_tree as qt

q_obj = qt.QuadObj(qt.distance_f, quad_type='pair', last_is_quad=True)
q_obj.create()
print(q_obj)