# -*- coding: utf-8 -*-

"""
simpleplots.visuals
~~~~~~~~~~~~~~~~~~~

"""

from .base import Coords

#-------------------------------------------------------------------------------

class Spines(object):

    def __init__(self, img_width, img_height, theme):
        self.img_width = img_width
        self.img_height = img_height
        self.theme = theme

        self.width = self.img_width * self.theme.spine_box_width_perc
        self.height = self.img_height * self.theme.spine_box_height_perc
        self.horizontal_offset = (self.img_width - self.width) / 2
        self.vertical_offset = (self.img_height - self.height) / 2

    @property
    def left(self):
        return Coords(
            self.horizontal_offset, self.vertical_offset,
            self.horizontal_offset, self.vertical_offset + self.height
        )

    @property
    def right(self):
        return Coords(
            self.horizontal_offset + self.width, self.vertical_offset,
            self.horizontal_offset + self.width, self.vertical_offset + self.height
        )

    @property
    def top(self):
        return Coords(
            self.horizontal_offset, self.vertical_offset,
            self.horizontal_offset + self.width, self.vertical_offset
        )

    @property
    def bottom(self):
        return Coords(
            self.horizontal_offset, self.vertical_offset + self.height,
            self.horizontal_offset + self.width, self.vertical_offset + self.height
        )

    @property
    def all(self):
        return [
            self.left,
            self.top,
            self.right,
            self.bottom
        ]

#-------------------------------------------------------------------------------

class PointsGrid(object):

    def __init__(self, spines_width, spines_height, theme):
        self.spines_width = spines_width
        self.spines_height = spines_height
        self.theme = theme

        self.width = self.spines_width * self.theme.grid_box_width_perc
        self.height = self.spines_height * self.theme.grid_box_height_perc
        self.horizontal_offset = (self.spines_width - self.width) / 2
        self.vertical_offset = (self.spines_height - self.height) / 2

        self.x_lines_number = None
        self.y_lines_number = None

#-------------------------------------------------------------------------------
