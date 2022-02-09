# -*- coding: utf-8 -*-

"""
simpleplots.ticker
~~~~~~~~~~~~~~~~~~

This module contains classes for configuring tick locating. `EdgeInteger` and
`MaxNLocator` located here are just a simplified version of what you can find
in matplotlib's (https://github.com/matplotlib/matplotlib) `ticker` module.

If you want to understand the logic of calculation it is recommended to check
matplotlib's original code!

"""

from .utils import scale_range

from decimal import *
import math

#-------------------------------------------------------------------------------

getcontext().prec = 6

#-------------------------------------------------------------------------------

class EdgeInteger(object):

    def __init__(self, step, offset):
        if step <= 0:
            raise ValueError("'step' must be positive")
        self.step = step
        self._offset = abs(offset)

    def closeto(self, ms, edge):
        if self._offset > 0:
            digits = math.log10(self._offset / self.step)
            tol = max(1e-10, 10 ** (digits - 12))
            tol = min(0.4999, tol)
        else:
            tol = 1e-10
        return abs(ms - edge) < tol

    def le(self, x):
        d, m = divmod(x, self.step)
        if self.closeto(m / self.step, 1):
            return d + 1
        return d

    def ge(self, x):
        d, m = divmod(x, self.step)
        if self.closeto(m / self.step, 0):
            return d
        return d + 1

class MaxNLocator(object):

    def __init__(self, nbins=10, steps=[1, 2, 4, 5, 10], integer=False, min_n_ticks=2):
        self._nbins = nbins
        self._steps = steps
        self._extended_steps = self._staircase(self._steps)
        self._integer = integer
        self._min_n_ticks = min_n_ticks

    @staticmethod
    def _staircase(steps):
        float_stairs = [0.1 * s for s in steps[:-1]]
        largest_value = [10 * steps[1]]
        staircase = list(set(float_stairs + steps + largest_value))
        return sorted(staircase)

    def _raw_ticks(self, vmin, vmax):
        scale, offset = scale_range(vmin, vmax, self._nbins)
        _vmin = vmin - offset
        _vmax = vmax - offset
        raw_step = (_vmax - _vmin) / self._nbins

        if scale < 1:
            steps = [Decimal(s) * Decimal(scale) for s in self._extended_steps]
            steps = [float(s.normalize()) for s in steps]
        else:
            steps = [s * scale for s in self._extended_steps]

        if self._integer:
            steps = [s for s in steps if s < 1 or int(s) - s == 0]

        istep = [i for i, s in enumerate(steps) if s >= raw_step][0]

        for istep in reversed(range(istep + 1)):
            step = steps[istep]

            if (self._integer and
                math.floor(_vmax) - math.ceil(_vmin) >= self._min_n_ticks - 1):
                step = max(1, step)
            best_vmin = (_vmin // step) * step

            edge = EdgeInteger(step, offset)
            low = edge.le(_vmin - best_vmin)
            high = edge.ge(_vmax - best_vmin)

            ticks = list()
            for t in range(int(low), int(high) + 1):
                if scale < 1:
                    tick = t * step + best_vmin
                    tick = float(Decimal(tick).normalize())
                else:
                    tick = t * step + best_vmin
                ticks.append(tick)

            nticks = len([t for t in ticks if t <= _vmax and t >= _vmin])
            if nticks >= self._min_n_ticks:
                break

        return [t + offset for t in ticks]

    def tick_values(self, vmin, vmax):
        if vmax < vmin:
            vmin, vmax = vmax, vmin

        locs = self._raw_ticks(vmin, vmax)
        return locs

#-------------------------------------------------------------------------------
