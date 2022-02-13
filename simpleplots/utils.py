# -*- coding: utf-8 -*-

"""
simpleplots.utils
~~~~~~~~~~~~~~~~~

This module contains simpleplots' utilities.

"""

__all__ = ('get_text_dimensions', 'normalize_float', 'decimals', 'isint',
           'normalize_values', 'scale_range', 'frange', 'smartrange', 'get_font')

from .base import Tuple, List, Union, Iterable

from PIL import ImageFont
from decimal import *
import numpy as np
import math
import os

getcontext().prec = 6

#-------------------------------------------------------------------------------

INT_DTYPES: List[str] = ['int8', 'int16', 'int32', 'int64']
FLOAT_DTYPES: List[str] = ['float16', 'float32', 'float64', 'float96', 'float128']

#-------------------------------------------------------------------------------

def get_font(type_, theme, image_width):
    package_directory_path = os.path.abspath(os.path.dirname(__file__))
    fonts_folder = os.path.join(package_directory_path, 'fonts')

    if type_ == 'tick_label':
        return ImageFont.truetype(
            os.path.join(fonts_folder, theme.tick_label_font),
            int(image_width * theme.tick_label_size_perc)
        )

    elif type_ == 'title':
        return ImageFont.truetype(
            os.path.join(fonts_folder, theme.title_font),
            int(image_width * theme.title_size_perc)
        )

#-------------------------------------------------------------------------------

def get_text_dimensions(text_string: str, font: ImageFont) -> Tuple[int, int]:
    """Calculates size of a given text string using given font."""
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

#-------------------------------------------------------------------------------

def normalize_float(n: float, r: int = 4) -> float:
    n = float(Decimal(n).normalize())
    n = round(n, r)
    return n

#-------------------------------------------------------------------------------

def decimals(n: float) -> int:
    return len(str(n).split('.')[1]) if len(str(n).split('.')) == 2 else 0

def isint(n: Union[int, float]) -> bool:
    return isinstance(n, int) or n.is_integer()

#-------------------------------------------------------------------------------

def normalize_values(values: List[Union[int, float]]) -> np.ndarray:
    values = np.asarray(values)

    if values.dtype in INT_DTYPES:
        return values

    elif values.dtype in FLOAT_DTYPES:
        values = np.around(values, decimals=4)
        return values

    else:
        raise TypeError('unknown input datatype')

#-------------------------------------------------------------------------------

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

def frange(start: float, stop: float, step: float = None) -> Iterable[float]:
    """Generates a range between float numbers."""
    start, stop = float(start), float(stop)
    if not step:
        start_scale = len(str(start).split('.')[1])
        stop_scale = len(str(stop).split('.')[1])
        scale = max(start_scale, stop_scale)
        step = 1 * (10 ** -scale)

    start, stop = Decimal(start).normalize(), Decimal(stop).normalize()

    while start <= stop:
        yield float(start)
        start += Decimal(step).normalize()

#-------------------------------------------------------------------------------

def smartrange(vmin: Union[int, float], vmax: Union[int, float],
               origin_values: np.ndarray) -> np.ndarray:
    """Fills gaps between vmin and vmax based on input type."""

    if isinstance(vmin, (float, int)) and isinstance(vmax, (float, int)):

        if (isint(vmin) and isint(vmax) and origin_values.dtype in INT_DTYPES):
            n_range = np.arange(int(vmin), int(vmax) + 1, 1)
            #-------------------------------------------------------------------
            if max([abs(n) for n in n_range]) <= 10 and len(n_range) <= 5:
                return np.asarray([i for i in frange(vmin, vmax, 0.1)])
            #-------------------------------------------------------------------
            return n_range

        else:
            start, stop = normalize_float(vmin), normalize_float(vmax)
            start_scale, stop_scale = decimals(start), decimals(stop)
            origin_scale = max([decimals(n) for n in origin_values])

            scale = max(start_scale, stop_scale, origin_scale)
            step = 1 * (10 ** -scale)

            return np.asarray([i for i in frange(vmin, vmax, step)])

#-------------------------------------------------------------------------------
