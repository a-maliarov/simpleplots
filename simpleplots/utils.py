# -*- coding: utf-8 -*-

"""
simpleplots.utils
~~~~~~~~~~~~~~~~~

This module contains simpleplots' utilities.

"""

__all__ = ('get_font', 'get_text_dimensions', 'normalize_float', 'find_gcd',
           'decimals', 'isint', 'normalize_values', 'frange', 'smartrange'
           'get_indices_of_values_in_list', 'choose_locator')

from .base import Theme, Size
from .ticker import Locator, AutoLocator, AutoFormatter
from .dates import AutoDateLocator, AutoDateFormatter

from typing import List, Iterable
from numpy.typing import ArrayLike
from numbers import Number
from PIL import ImageFont

from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from functools import reduce
from decimal import *
import numpy as np
import math
import os

getcontext().prec = 6

#-------------------------------------------------------------------------------

DISPLAYABLE: int = 15360 # maximum number of elements per axis
INT_DTYPES: List[str] = ['int8', 'int16', 'int32', 'int64']
FLOAT_DTYPES: List[str] = ['float16', 'float32', 'float64', 'float96', 'float128']
DATE_DTYPE: str = 'datetime64'

#-------------------------------------------------------------------------------

def get_font(type_: str, theme: Theme, image_width: int) -> ImageFont:
    """Return ImageFont based theme, type and image width."""
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

def get_text_dimensions(text_string: str, font: ImageFont) -> Size:
    """Calculates size of a given text string using given font."""
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

#-------------------------------------------------------------------------------

def normalize_float(n: float) -> float:
    """Normalize floats like '1.230000000003' to just '1.23'."""
    return float(Decimal(n).normalize())

def find_gcd(lst: List[int]) -> int:
    """Find GCD of a list."""
    return reduce(math.gcd, lst)

def decimals(n: float) -> int:
    """Get the number of decimals after comma."""
    if 'e' in str(n):
        return int(str(n).split('e')[1][1:])
    return len(str(n).split('.')[1]) if len(str(n).split('.')) == 2 else 0

def isint(n: Number) -> bool:
    """Check if number is integer even if type if float."""
    return isinstance(n, int) or n.is_integer()

#-------------------------------------------------------------------------------

def get_indices_of_values_in_list(values: np.ndarray, lst: np.ndarray) -> np.ndarray:
    """Get indices of values in list A from list B."""
    sorter = np.argsort(lst)
    ind = sorter[np.searchsorted(lst, values, sorter=sorter)]
    return ind

#-------------------------------------------------------------------------------

def normalize_values(values: ArrayLike) -> np.ndarray:
    """Check input values before trying to plot them."""
    values = np.asarray(values)

    if values.dtype in INT_DTYPES:
        step = find_gcd(values)
        max_value = np.max(values)

        if max_value / step / DISPLAYABLE > 3:
            round_to = int(math.log10(int(max_value / step / DISPLAYABLE))) + 1
            values = np.around(values, decimals=-round_to)

        return values

    elif values.dtype in FLOAT_DTYPES:
        scale = max([decimals(normalize_float(n)) for n in values])
        step = 1 * (10 ** -scale)
        max_value = normalize_float(np.max(values))

        if max_value / step / DISPLAYABLE > 3:
            round_to = int(math.log10(int(max_value / step / DISPLAYABLE))) + 1
            values = np.around(values, decimals=round_to)

        return np.asarray([normalize_float(n) for n in values])

    elif all([isinstance(e, datetime) for e in values]):
        values = values.astype('datetime64[s]')
        return values

    elif DATE_DTYPE in str(values.dtype):
        values = values.astype('datetime64[s]')
        return values

    else:
        raise TypeError('unknown input datatype')

#-------------------------------------------------------------------------------

def choose_locator(values: np.ndarray) -> Locator:
    """Returns tick locator based on datatype."""
    if values.dtype in INT_DTYPES or values.dtype in FLOAT_DTYPES:
        return AutoLocator()
    elif DATE_DTYPE in str(values.dtype):
        return AutoDateLocator()
    else:
        raise TypeError('unknown input datatype')

def choose_formatter(values: np.ndarray) -> Locator:
    """Returns label formatter based on datatype."""
    if values.dtype in INT_DTYPES or values.dtype in FLOAT_DTYPES:
        return AutoFormatter()
    elif DATE_DTYPE in str(values.dtype):
        return AutoDateFormatter()
    else:
        raise TypeError('unknown input datatype')

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

def find_min_timedelta(values: np.ndarray) -> dict:
    """Given an array of dates, finds the minimum timedelta parameters."""
    datetime_values = [d.astype(datetime) for d in values]

    params = {
        'seconds': 0,
        'minutes': 0,
        'hours': 0,
        'days': 0,
        'months': 0,
        'years': 0
    }

    changes = {
        'seconds': 0,
        'minutes': 0,
        'hours': 0,
        'days': 0,
        'months': 0,
        'years': 0
    }

    if (any(d.second for d in datetime_values) and not
        all(d.second == datetime_values[0].second for d in datetime_values)):
        changes['seconds'] = 1

    if (any(d.minute for d in datetime_values) and not
        all(d.minute == datetime_values[0].minute for d in datetime_values)):
        changes['minutes'] = 1

    if (any(d.hour for d in datetime_values) and not
        all(d.hour == datetime_values[0].hour for d in datetime_values)):
        changes['hours'] = 1

    if (any(d.day for d in datetime_values) and not
        all(d.day == datetime_values[0].day for d in datetime_values)):
        changes['days'] = 1

    if (any(d.month for d in datetime_values) and not
        all(d.month == datetime_values[0].month for d in datetime_values)):
        changes['months'] = 1

    if (any(d.year for d in datetime_values) and not
        all(d.year == datetime_values[0].year for d in datetime_values)):
        changes['years'] = 1

    if changes['years'] or changes['months']:
        params['days'] = 1
    elif changes['days']:
        params['hours'] = 1
    elif changes['hours']:
        params['minutes'] = 1
    elif changes['minutes']:
        params['seconds'] = 1

    return params

#-------------------------------------------------------------------------------

def smartrange(vmin: Number, vmax: Number, origin_values: np.ndarray) -> np.ndarray:
    """Fills gaps between vmin and vmax based on input type."""

    if isinstance(vmin, (float, int)) and isinstance(vmax, (float, int)):

        if (isint(vmin) and isint(vmax) and origin_values.dtype in INT_DTYPES):
            all_values = np.append(origin_values, [int(vmin), int(vmax)])
            step = find_gcd(all_values)
            n_range = np.arange(int(vmin), int(vmax) + 1, step)
            #-------------------------------------------------------------------
            if max([abs(n) for n in n_range]) <= 10 and len(n_range) <= 5:
                return np.asarray([i for i in frange(vmin, vmax, 0.1)])
            #-------------------------------------------------------------------
            return n_range

        else:
            start, stop = normalize_float(vmin), normalize_float(vmax)
            start_scale, stop_scale = decimals(start), decimals(stop)
            origin_values = np.asarray([float(n) for n in origin_values])
            origin_scale = max([decimals(normalize_float(n)) for n in origin_values])

            scale = max(start_scale, stop_scale, origin_scale)
            step = 1 * (10 ** -scale)

            return np.asarray([i for i in frange(vmin, vmax, step)])

    elif DATE_DTYPE in str(origin_values.dtype):
        params = find_min_timedelta(origin_values)
        dmin, dmax = np.min(origin_values), np.max(origin_values)
        values = np.arange(dmin, dmax, relativedelta(**params), dtype='datetime64[s]')
        values = np.append(values, dmax)

        return values

#-------------------------------------------------------------------------------
