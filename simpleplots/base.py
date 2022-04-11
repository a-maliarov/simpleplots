# -*- coding: utf-8 -*-

"""
simpleplots.base
~~~~~~~~~~~~~~~~

This module contains all the dataclasses.

"""

__all__ = ('Coords', 'Theme', 'Axes', 'Point', 'Size')

from typing import Tuple, NamedTuple
from dataclasses import dataclass, field
from numbers import Number
import numpy as np

#-------------------------------------------------------------------------------

class Size(NamedTuple):
    width: int
    height: int

class Point(NamedTuple):
    x: Number
    y: Number

class Coords(NamedTuple):
    x0: Number
    y0: Number
    x1: Number
    y1: Number

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
    xvalues: np.ndarray
    yvalues: np.ndarray
    color: str = 'red'
    linewidth: int = 4
    points: np.ndarray = field(init=False)

    def __post_init__(self):
        values = np.asarray([self.xvalues, self.yvalues])
        self.points = np.dstack(values)[0]

#-------------------------------------------------------------------------------
