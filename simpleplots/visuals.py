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

    def __init__(self, spines, theme):
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

        self.x_connections = list()
        self.y_connections = list()

    def configure_size(self):
        self.cell_width = self.width / (len(self.xvalues) - 1)
        self.cell_height = self.height / (len(self.yvalues) - 1)

    def map_values_with_coords(self):
        self.x_connections = list()
        for x_index, x_value in enumerate(self.xvalues):
            x_coordinate = self.spines.horizontal_offset + self.horizontal_offset + (self.cell_width * x_index + 1)

            point_data = {
                'point_value': x_value,
                'point_coords': x_coordinate
            }
            self.x_connections.append(point_data)

        self.y_connections = list()
        for y_index, y_value in enumerate(self.yvalues):
            y_coordinate = self.spines.vertical_offset + self.vertical_offset + (self.cell_height * (len(self.yvalues) - y_index - 1))

            point_data = {
                'point_value': y_value,
                'point_coords': y_coordinate
            }
            self.y_connections.append(point_data)

#-------------------------------------------------------------------------------
