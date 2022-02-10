# -*- coding: utf-8 -*-

"""
simpleplots.visuals
~~~~~~~~~~~~~~~~~~~

This module contains Spines and GridPoints instances responsible for connection
between axes' values and image coordinates.

"""

__all__ = ('Spines', 'PointsGrid')

from .base import Coords, Theme, List

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

        self.xvalues = list()
        self.yvalues = list()

        self.x_major_ticks = list()
        self.x_major_ticks = list()

        self.cell_width = None
        self.cell_height = None

        self.x_connections = dict()
        self.y_connections = dict()

    def configure_size(self) -> None:
        """
        Calculates the distance between two points on an image. Say, grid width
        is 100px, while x-axis values are [1, 2, 3, 4, 5]. Values should be
        displayed at 0px, 25px, 50px, 75px and 100px accordingly. This step of
        25px is what this function calculates.

        """

        self.cell_width = self.width / (len(self.xvalues) - 1)
        self.cell_height = self.height / (len(self.yvalues) - 1)

    def map_values_with_coords(self) -> None:
        """
        Saves axes' connections based on the distance between values, so later,
        when we have, say, y-100, we can access grid.y_connections dictionary
        using the value as a key and get the coordinate.

        """

        self.x_connections = dict()
        for x_index, x_value in enumerate(self.xvalues):
            x_coordinate = self.spines.horizontal_offset + self.horizontal_offset \
                         + (self.cell_width * x_index + 1)
            self.x_connections[x_value] = x_coordinate

        self.y_connections = dict()
        for y_index, y_value in enumerate(self.yvalues):
            y_coordinate = self.spines.vertical_offset + self.vertical_offset \
                         + self.cell_height * (len(self.yvalues) - y_index - 1)
            self.y_connections[y_value] = y_coordinate

#-------------------------------------------------------------------------------
