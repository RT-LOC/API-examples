"""
    RTLOC - Engine

    engine.py

    (c) 2021-2022 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>
    Frederic Mes   <fred@rtloc.com>

"""

from scipy.optimize import minimize
import math
import numpy as np

class Position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)

class DebugPostionEngine:
    def __init__(self, nb_anchors):
        self.sse = 0
        self.nb_anchors = nb_anchors

    def set_anchor_positions(self, anchor_positions):
        self.anchor_positions = anchor_positions

    def compute_tag_position(self, measurements, initial_position):
        return self._optimize(measurements, [initial_position.x, initial_position.y]) # + initial_position.corrections)

    def get_sse(self):
        return self.sse

    def _mse(self, x, locations, distances):
        mse = 0.0
        for idx, (location, distance) in enumerate(zip(locations, distances)):
            distance_calculated = math.sqrt((x[0] - location.x)**2 + (x[1] - location.y)**2)
            mse += (distance_calculated - distance)**2 # - x[2+idx])**2

        # mse += np.sum(np.abs(x[2:]))**2
        if(len(distances) > 0):
            return mse / len(distances)
        else:
            return 0
    def _optimize(self, measurements, initial_position):
        result = minimize(
            self._mse,
            initial_position,
            args=(self.anchor_positions, measurements),
            method='L-BFGS-B',
            options={
                'ftol':1e-1,
                'maxiter': 10
            })

        self.sse = result.fun

        # if not result.success:
        #     print("opt not succeeded", result.message)

        pos = Position(result.x[0], result.x[1], 0)
        # pos.corrections = result.x[2:]

        return pos
