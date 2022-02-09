# -*- coding: utf-8 -*-

"""
simpleplots.utils
~~~~~~~~~~~~~~~~~

"""

from decimal import *
import math
import os

getcontext().prec = 6

#-------------------------------------------------------------------------------

def get_text_dimensions(text_string, font):
    # https://gist.github.com/Ze1598/420c7eb600899c86d1d65e83c3cc8b25
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

#-------------------------------------------------------------------------------

def frange(start, stop, step=None):
    start, stop = float(start), float(stop)
    if not step:
        start_scale = len(str(start).split('.')[1])
        stop_scale = len(str(stop).split('.')[1])
        scale = max(start_scale, stop_scale)
        step = 1 * (10 ** -scale)

    start, stop = Decimal(start), Decimal(stop)

    while start <= stop:
        yield float(start)
        start += Decimal(step).normalize()

#-------------------------------------------------------------------------------

def scale_range(vmin, vmax, n=1, threshold=100):
    dv = abs(vmax - vmin)
    meanv = (vmax + vmin) / 2
    if abs(meanv) / dv < threshold:
        offset = 0
    else:
        offset = math.copysign(10 ** (math.log10(abs(meanv)) // 1), meanv)
    scale = 10 ** (math.log10(dv / n) // 1)

    return scale, offset

#-------------------------------------------------------------------------------

def smartrange(vmin, vmax, origin_values):
    if isinstance(vmin, float) and isinstance(vmax, float):

        all_integers = all([isinstance(n, int) or n.is_integer() for n in origin_values])
        if vmin.is_integer() and vmax.is_integer() and all_integers:
            n_range = list(range(int(vmin), int(vmax) + 1))
            #-------------------------------------------------------------------
            if max([abs(n) for n in n_range]) <= 10 and len(n_range) <= 5:
                return [n for n in frange(vmin, vmax, 0.1)]
            #-------------------------------------------------------------------
            return n_range

        else:
            start, stop = float(vmin), float(vmax)
            start_scale = len(str(start).split('.')[1])
            stop_scale = len(str(stop).split('.')[1])

            origin_floats = [len(str(n).split('.')[1]) for n in origin_values if len(str(n).split('.')) == 2]
            origin_scale = max(origin_floats) if origin_floats else 0

            scale = max(start_scale, stop_scale, origin_scale)
            step = 1 * (10 ** -scale)
            return [n for n in frange(vmin, vmax, step)]

#-------------------------------------------------------------------------------
