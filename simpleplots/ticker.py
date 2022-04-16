# -*- coding: utf-8 -*-

"""
simpleplots.ticker
~~~~~~~~~~~~~~~~~~

This module contains classes for configuring tick values. `EdgeInteger` and
`AutoLocator` located here are just a simplified version of what you can find
in matplotlib's (https://github.com/matplotlib/matplotlib) `ticker` module.

If you want to understand the logic of calculation it is recommended to check
matplotlib's original code!

"""

__all__ = ('Locator', 'AutoLocator', 'NullFormatter', 'AutoFormatter')

from decimal import *
import numpy as np
import math

getcontext().prec = 6

#-------------------------------------------------------------------------------

def normalize_float(n: float) -> float:
    """Normalize floats like '1.230000000003' to just '1.23'."""
    return float(Decimal(n).normalize())

def scale_range(vmin: float, vmax: float, n: int = 1, threshold: int = 100):
    """Identifies the maximum scale of the given range."""
    dv = abs(vmax - vmin)
    meanv = (vmax + vmin) / 2
    if abs(meanv) / dv < threshold:
        offset = 0
    else:
        offset = math.copysign(10 ** (math.log10(abs(meanv)) // 1), meanv)
    scale = 10 ** (math.log10(dv / n) // 1)

    return scale, offset

#-------------------------------------------------------------------------------

class EdgeInteger(object):

    def __init__(self, step, offset):
        if step <= 0:
            raise ValueError("'step' must be positive")
        self.step = step
        self._offset = abs(offset)

    def closeto(self, ms, edge):
        if self._offset > 0:
            digits = np.log10(self._offset / self.step)
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

#-------------------------------------------------------------------------------

class Formatter(object):
    rotation = 0

    def __call__(self, value):
        """Return the label for the given tick value."""
        raise NotImplementedError('Derived must override')

class NullFormatter(Formatter):

    def __call__(self, value):
        """Always return the empty string."""
        return ''

class AutoFormatter(Formatter):

    def __call__(self, value):
        return str(value)

#-------------------------------------------------------------------------------

class Locator(object):

    def tick_values(self, vmin, vmax):
        raise NotImplementedError('Derived must override')

class AutoLocator(Locator):

    def __init__(self, nbins=10, steps=[1, 2, 4, 5, 10], integer=False, min_n_ticks=2):
        self._nbins = nbins
        self._steps = self._validate_steps(steps)
        self._extended_steps = self._staircase(self._steps)
        self._integer = integer
        self._min_n_ticks = min_n_ticks

    @staticmethod
    def _validate_steps(steps):
        if not np.iterable(steps):
            raise ValueError('steps argument must be an increasing sequence '
                             'of numbers between 1 and 10 inclusive')
        steps = np.asarray(steps)
        if np.any(np.diff(steps) <= 0) or steps[-1] > 10 or steps[0] < 1:
            raise ValueError('steps argument must be an increasing sequence '
                             'of numbers between 1 and 10 inclusive')
        if steps[0] != 1:
            steps = np.concatenate([[1], steps])
        if steps[-1] != 10:
            steps = np.concatenate([steps, [10]])
        return steps

    @staticmethod
    def _staircase(steps):
        return np.concatenate([0.1 * steps[:-1], steps, [10 * steps[1]]])

    def _raw_ticks(self, vmin, vmax):
        scale, offset = scale_range(vmin, vmax, self._nbins)
        _vmin = vmin - offset
        _vmax = vmax - offset
        raw_step = (_vmax - _vmin) / self._nbins
        steps = self._extended_steps * scale

        if self._integer:
            igood = (steps < 1) | (np.abs(steps - np.round(steps)) < 0.001)
            steps = steps[igood]

        istep = np.nonzero(steps >= raw_step)[0][0]

        for istep in reversed(range(istep + 1)):
            step = steps[istep]

            if (self._integer and
                    np.floor(_vmax) - np.ceil(_vmin) >= self._min_n_ticks - 1):
                step = max(1, step)
            best_vmin = (_vmin // step) * step

            edge = EdgeInteger(step, offset)
            low = edge.le(_vmin - best_vmin)
            high = edge.ge(_vmax - best_vmin)

            ticks = np.arange(low, high + 1) * step + best_vmin
            ticks = np.asarray([normalize_float(i) for i in ticks])
            nticks = ((ticks <= _vmax) & (ticks >= _vmin)).sum()

            if nticks >= self._min_n_ticks:
                break

        return ticks + offset

    def tick_values(self, vmin, vmax):
        if vmax < vmin:
            vmin, vmax = vmax, vmin
        elif vmin == vmax:
            return [vmin]

        locs = self._raw_ticks(vmin, vmax)
        return locs

#-------------------------------------------------------------------------------
