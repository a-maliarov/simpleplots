# -*- coding: utf-8 -*-

"""
simpleplots.visuals
~~~~~~~~~~~~~~~~~~~

This module contains Spines and GridPoints instances responsible for connection
between axes' values and image coordinates.

"""

__all__ = ('Spines', 'PointsGrid')

from .base import Coords, Theme, Point
from .utils import get_text_dimensions

from numbers import Number
from PIL import Image, ImageFont, ImageDraw
from typing import List

#-------------------------------------------------------------------------------

class CustomImageDraw(ImageDraw.ImageDraw):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def rtext(self, *args, **kwargs):
        """Allows drawing rotated text."""
        rotation = kwargs.pop('rotation')

        if not rotation:
            self.text(*args, **kwargs)

        else:
            xy = kwargs.pop('xy')
            text = kwargs.pop('text')
            font = kwargs.pop('font')
            fill = kwargs.pop('fill')

            text_width, text_height = get_text_dimensions(text, font)

            mask = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(mask)
            draw.text((0, 0), text=text, font=font, fill=(*fill, 255))
            mask = mask.rotate(rotation, expand=True)

            x = int(xy[0]) - mask.size[0] + int(mask.size[0] * 0.1)
            y = int(xy[1]) - int(mask.size[1] * 0.1)
            self._image.paste(mask, (x, y), mask)

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

        self.horizontal_offset *= 1 + self.theme.spine_box_add_hor_offset
        self.vertical_offset /= 1 + self.theme.spine_box_add_ver_offset

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

        self.full_h_offset = self.spines.horizontal_offset + self.horizontal_offset
        self.full_v_offset = self.spines.vertical_offset + self.vertical_offset

        self.tick_length = self.spines.width * self.theme.tick_length_perc

        self.xvalues = None
        self.yvalues = None

        self.x_major_ticks = None
        self.x_major_ticks = None

        self.cell_width = None
        self.cell_height = None

    def get_x_line_coords(self, x_index: int) -> Coords:
        """Get coordinates of internal grid vertical line."""
        return Coords(
            self.full_h_offset + self.cell_width * x_index,
            self.spines.vertical_offset,
            self.full_h_offset + self.cell_width * x_index,
            self.full_v_offset + self.vertical_offset + self.height
        )

    def get_y_line_coords(self, y_index: int) -> Coords:
        """Get coordinates of internal grid horizontal line."""
        return Coords(
            self.spines.horizontal_offset,
            self.full_v_offset + self.height - self.cell_height * y_index,
            self.full_h_offset + self.horizontal_offset + self.width,
            self.full_v_offset + self.height - self.cell_height * y_index
        )

    def get_x_tick_coords(self, x_index: int) -> Coords:
        """Get coordinates of vertically oriented tick."""
        return Coords(
            self.full_h_offset + self.cell_width * x_index,
            self.full_v_offset + self.vertical_offset + self.height,
            self.full_h_offset + self.cell_width * x_index,
            self.full_v_offset + self.vertical_offset + self.height + self.tick_length
        )

    def get_y_tick_coords(self, y_index: int) -> Coords:
        """Get coordinates of horizontally oriented tick."""
        return Coords(
            self.spines.horizontal_offset - self.tick_length,
            self.full_v_offset + self.height - self.cell_height * y_index,
            self.spines.horizontal_offset,
            self.full_v_offset + self.height - self.cell_height * y_index
        )

    def get_x_tick_label_coords(self, x_index: int, text: str,
                                font: ImageFont) -> Point:
        """Get coordinates of X tick label."""
        text_width, text_height = get_text_dimensions(text, font)

        return Point(
            self.full_h_offset + self.cell_width * x_index,
            self.full_v_offset + self.vertical_offset + self.height \
                                        + self.tick_length * 2      \
                                        + text_height / 2,
        )

    def get_y_tick_label_coords(self, y_index: int, text: str,
                                font: ImageFont) -> Point:
        """Get coordinates of Y tick label."""
        text_width, text_height = get_text_dimensions(text, font)

        return Point(
            self.spines.horizontal_offset - self.tick_length * 2 - text_width / 2,
            self.full_v_offset + self.height - self.cell_height * y_index,
        )

    def get_title_coords(self, text: str, font: ImageFont) -> Point:
        """Get coordinates of title position on the image."""
        text_width, text_height = get_text_dimensions(text, font)

        return Point(
            self.full_h_offset + self.width / 2,
            self.spines.vertical_offset - self.tick_length * 2 - text_height / 2,
        )

    def get_x_point_coords(self, x_index: int) -> Number:
        """Get coordinates of point on x-axis by X index."""
        return self.full_h_offset + self.cell_width * x_index

    def get_y_point_coords(self, y_index: int) -> Number:
        """Get coordinates of point on y-axis by Y index."""
        return self.full_v_offset + self.height - self.cell_height * y_index

    def get_point_coords(self, x_index: int, y_index: int) -> Point:
        """Get coordinates of point by X and Y indices."""
        x_coords = self.get_x_point_coords(x_index)
        y_coords = self.get_y_point_coords(y_index)
        return Point(x_coords, y_coords)

#-------------------------------------------------------------------------------
