# -*- coding: utf-8 -*-

"""
simpleplots.base
~~~~~~~~~~~~~~~~

This module contains all the dataclasses.

"""

__all__ = ('Coords', 'Theme', 'Axes')

from typing import Tuple
from dataclasses import dataclass, field
from collections import namedtuple
import numpy as np

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
    values: np.ndarray
    color: str = 'red'
    linewidth: int = 4
    points: np.ndarray = field(init=False)

    def __post_init__(self):
        self.points = np.dstack(self.values)[0]

#-------------------------------------------------------------------------------
