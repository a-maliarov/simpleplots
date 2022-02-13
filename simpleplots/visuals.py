# -*- coding: utf-8 -*-

"""
simpleplots.visuals
~~~~~~~~~~~~~~~~~~~

This module contains Spines and GridPoints instances responsible for connection
between axes' values and image coordinates.

"""

__all__ = ('Spines', 'PointsGrid')

from .base import Coords, Theme
from .utils import get_text_dimensions

from typing import List
import numpy as np

#-------------------------------------------------------------------------------

class Spines(object):

    def __init__(self, img_width: int, img_height: int, theme: Theme) -> None:
        """
        Initializes Spines instance responsible for graph's spines box and
        coordinates of each spine based on the image size and theme.

        """

        self.img_width = img_width
        self.img_height = img_height
        self.theme = theme

        self.width = self.img_width * self.theme.spine_box_width_perc
        self.height = self.img_height * self.theme.spine_box_height_perc
        self.horizontal_offset = (self.img_width - self.width) / 2
        self.vertical_offset = (self.img_height - self.height) / 2

    @property
    def left(self) -> Coords:
        """Coordinates of the left spine."""
        return Coords(
            self.horizontal_offset, self.vertical_offset,
            self.horizontal_offset, self.vertical_offset + self.height
        )

    @property
    def right(self) -> Coords:
        """Coordinates of the right spine."""
        return Coords(
            self.horizontal_offset + self.width, self.vertical_offset,
            self.horizontal_offset + self.width, self.vertical_offset + self.height
        )

    @property
    def top(self) -> Coords:
        """Coordinates of the top spine."""
        return Coords(
            self.horizontal_offset, self.vertical_offset,
            self.horizontal_offset + self.width, self.vertical_offset
        )

    @property
    def bottom(self) -> Coords:
        """Coordinates of the bottom spine."""
        return Coords(
            self.horizontal_offset, self.vertical_offset + self.height,
            self.horizontal_offset + self.width, self.vertical_offset + self.height
        )

    @property
    def all(self) -> List[Coords]:
        """List of all spines coordinates."""
        return [
            self.left,
            self.top,
            self.right,
            self.bottom
        ]

#-------------------------------------------------------------------------------

class PointsGrid(object):

    def __init__(self, spines: Spines, theme: Theme) -> None:
        """
        Initializes PointsGrid instance responsible mainly for the connection
        between axes' values and image coordinates.

        """

        self.spines = spines
        self.theme = theme

        self.width = self.spines.width * self.theme.grid_box_width_perc
        self.height = self.spines.height * self.theme.grid_box_height_perc
        self.horizontal_offset = (self.spines.width - self.width) / 2
        self.vertical_offset = (self.spines.height - self.height) / 2

        self.tick_length = self.spines.width * self.theme.tick_length_perc

        self.xvalues = None
        self.yvalues = None

        self.x_major_ticks = None
        self.x_major_ticks = None

        self.cell_width = None
        self.cell_height = None

    def get_x_line_coords(self, x_index):
        return Coords(
            self.spines.horizontal_offset + self.horizontal_offset \
                                          + self.cell_width * x_index,
            self.spines.vertical_offset,
            self.spines.horizontal_offset + self.horizontal_offset \
                                          + self.cell_width * x_index,
            self.spines.vertical_offset + self.vertical_offset * 2 \
                                        + self.height
        )

    def get_y_line_coords(self, y_index):
        return Coords(
            self.spines.horizontal_offset,
            self.spines.vertical_offset + self.vertical_offset + self.height \
                                        - self.cell_height * y_index,
            self.spines.horizontal_offset + self.horizontal_offset * 2       \
                                          + self.width,
            self.spines.vertical_offset + self.vertical_offset + self.height
                                        - self.cell_height * y_index         \
        )

    def get_x_tick_coords(self, x_index):
        return Coords(
            self.spines.horizontal_offset + self.horizontal_offset \
                                          + self.cell_width * x_index,
            self.spines.vertical_offset + self.vertical_offset * 2 \
                                        + self.height,
            self.spines.horizontal_offset + self.horizontal_offset \
                                          + self.cell_width * x_index,
            self.spines.vertical_offset + self.vertical_offset * 2 \
                                        + self.height + self.tick_length
        )

    def get_y_tick_coords(self, y_index):
        return Coords(
            self.spines.horizontal_offset - self.tick_length,
            self.spines.vertical_offset + self.vertical_offset + self.height \
                                        - self.cell_height * y_index,
            self.spines.horizontal_offset,
            self.spines.vertical_offset + self.vertical_offset + self.height \
                                        - self.cell_height * y_index
        )

    def get_x_tick_label_coords(self, x_index, text, font):
        text_width, text_height = get_text_dimensions(text, font)

        return (
            self.spines.horizontal_offset + self.horizontal_offset \
                                          + self.cell_width * x_index,
            self.spines.vertical_offset + self.vertical_offset * 2 \
                                        + self.height              \
                                        + self.tick_length * 2     \
                                        + text_height / 2,
        )

    def get_y_tick_label_coords(self, y_index, text, font):
        text_width, text_height = get_text_dimensions(text, font)

        return (
            self.spines.horizontal_offset - self.tick_length * 2             \
                                          - text_width / 2,
            self.spines.vertical_offset + self.vertical_offset + self.height \
                                        - self.cell_height * y_index,
        )

    def get_title_coords(self, text, font):
        text_width, text_height = get_text_dimensions(text, font)

        return (
            self.spines.horizontal_offset + self.horizontal_offset \
                                          + self.width / 2,
            self.spines.vertical_offset - self.tick_length * 2     \
                                        - text_height / 2,
        )

    def get_x_point_coords(self, x_index):
        return self.spines.horizontal_offset + self.horizontal_offset \
                                             + (self.cell_width * x_index + 1)

    def get_y_point_coords(self, y_index):
        return self.spines.vertical_offset + self.vertical_offset \
                        + self.cell_height * (len(self.yvalues) - y_index - 1)

    def get_point_coords(self, x_index, y_index):
        x_coords = self.get_x_point_coords(x_index)
        y_coords = self.get_y_point_coords(y_index)
        return (x_coords, y_coords)

#-------------------------------------------------------------------------------
