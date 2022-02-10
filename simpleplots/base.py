# -*- coding: utf-8 -*-

"""
simpleplots.base
~~~~~~~~~~~~~~~~

This module contains all the dataclasses.

"""

__all__ = ('Theme', 'Axes', 'Tuple', 'List', 'Iterable', 'Union')

from dataclasses import dataclass
from collections import namedtuple
from typing import Tuple, List, Iterable, Union

#-------------------------------------------------------------------------------

Coords = namedtuple("Coords", "x0 y0 x1 y1")

#-------------------------------------------------------------------------------

@dataclass
class Theme:
    figure_background_color: Tuple[int, ...]

    spine_box_width_perc: float
    spine_box_height_perc: float
    spine_color: Tuple[int, ...]
    spine_width: float

    grid_box_width_perc: float
    grid_box_height_perc: float
    grid_visibility: bool
    grid_line_color: Tuple[int, ...]
    grid_line_width: float

    tick_length_perc: float
    tick_line_color: Tuple[int, ...]
    tick_line_width: float

    tick_label_font: str
    tick_label_size_perc: float
    tick_label_color: Tuple[int, ...]

    point_radius: float

    title_font: str
    title_size_perc: float
    title_color: Tuple[int, ...]

#-------------------------------------------------------------------------------

@dataclass
class Axes():
    xvalues: List[Union[int, float]]
    yvalues: List[Union[int, float]]
    color: str = 'red'
    linewidth: int = 4

#-------------------------------------------------------------------------------
