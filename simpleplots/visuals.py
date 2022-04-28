# -*- coding: utf-8 -*-

"""
simpleplots.visuals
~~~~~~~~~~~~~~~~~~~

This module contains Spines and GridPoints instances responsible for connection
between axes' values and image coordinates.

"""

__all__ = ('Spines', 'PointsGrid')

from .base import Coords, Theme, Point, Axes
from .utils import (get_text_dimensions, get_indices_of_values_in_list)

from numbers import Number
from PIL import Image, ImageFont, ImageDraw
from typing import List
import numpy as np

#-------------------------------------------------------------------------------

def _point_in_bbox(point: Point, bbox: Coords) -> bool:
    if (bbox.x0 <= point.x and point.x <= bbox.x1 and
        bbox.y0 <= point.y and point.y <= bbox.y1):

        return True

    else:
        return False

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
        _x_offset = self.cell_width * x_index
        if len(self.x_major_ticks) == 1:
            _x_offset = self.cell_width * 0.5

        return Coords(
            self.full_h_offset + _x_offset,
            self.spines.vertical_offset,
            self.full_h_offset + _x_offset,
            self.full_v_offset + self.vertical_offset + self.height
        )

    def get_y_line_coords(self, y_index: int) -> Coords:
        """Get coordinates of internal grid horizontal line."""
        _y_offset = self.cell_height * y_index
        if len(self.y_major_ticks) == 1:
            _y_offset = self.cell_height * 0.5

        return Coords(
            self.spines.horizontal_offset,
            self.full_v_offset + self.height - _y_offset,
            self.full_h_offset + self.horizontal_offset + self.width,
            self.full_v_offset + self.height - _y_offset
        )

    def get_x_tick_coords(self, x_index: int) -> Coords:
        """Get coordinates of vertically oriented tick."""
        _x_offset = self.cell_width * x_index
        if len(self.x_major_ticks) == 1:
            _x_offset = self.cell_width * 0.5

        return Coords(
            self.full_h_offset + _x_offset,
            self.full_v_offset + self.vertical_offset + self.height,
            self.full_h_offset + _x_offset,
            self.full_v_offset + self.vertical_offset + self.height + self.tick_length
        )

    def get_y_tick_coords(self, y_index: int) -> Coords:
        """Get coordinates of horizontally oriented tick."""
        _y_offset = self.cell_height * y_index
        if len(self.y_major_ticks) == 1:
            _y_offset = self.cell_height * 0.5

        return Coords(
            self.spines.horizontal_offset - self.tick_length,
            self.full_v_offset + self.height - _y_offset,
            self.spines.horizontal_offset,
            self.full_v_offset + self.height - _y_offset
        )

    def get_x_tick_label_coords(self, x_index: int, text: str,
                                font: ImageFont) -> Point:
        """Get coordinates of X tick label."""
        _x_offset = self.cell_width * x_index
        if len(self.x_major_ticks) == 1:
            _x_offset = self.cell_width * 0.5

        text_width, text_height = get_text_dimensions(text, font)

        return Point(
            self.full_h_offset + _x_offset,
            self.full_v_offset + self.vertical_offset + self.height \
                                        + self.tick_length * 2      \
                                        + text_height / 2,
        )

    def get_y_tick_label_coords(self, y_index: int, text: str,
                                font: ImageFont) -> Point:
        """Get coordinates of Y tick label."""
        _y_offset = self.cell_height * y_index
        if len(self.y_major_ticks) == 1:
            _y_offset = self.cell_height * 0.5

        text_width, text_height = get_text_dimensions(text, font)

        return Point(
            self.spines.horizontal_offset - self.tick_length * 2 - text_width / 2,
            self.full_v_offset + self.height - _y_offset,
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
        _x_offset = self.cell_width * x_index
        if len(self.x_major_ticks) == 1:
            _x_offset = self.cell_width * 0.5
        return self.full_h_offset + _x_offset

    def get_y_point_coords(self, y_index: int) -> Number:
        """Get coordinates of point on y-axis by Y index."""
        _y_offset = self.cell_height * y_index
        if len(self.y_major_ticks) == 1:
            _y_offset = self.cell_height * 0.5
        return self.full_v_offset + self.height - _y_offset

    def get_point_coords(self, x_index: int, y_index: int) -> Point:
        """Get coordinates of point by X and Y indices."""
        x_coords = self.get_x_point_coords(x_index)
        y_coords = self.get_y_point_coords(y_index)
        return Point(x_coords, y_coords)

    def get_axes_points_coords(self, axes: Axes) -> List[Point]:
        """Get coordinates of all points within axes."""
        px = get_indices_of_values_in_list(axes.xvalues, self.xvalues)
        py = get_indices_of_values_in_list(axes.yvalues, self.yvalues)

        xy_indices = np.dstack(np.asarray([px, py]))[0]
        return np.asarray([self.get_point_coords(x, y) for x, y in xy_indices])

    def get_legend_bbox(self, axes: List[Axes], font: ImageFont) -> dict:
        """Returns coordinates of legend mask."""
        priority = {
            '00': 0, '10': 6, '20': 1,
            '01': 4, '11': 8, '21': 5,
            '02': 2, '12': 7, '22': 3
        }

        sections = [
            {'anchor': 'la'}, {'anchor': 'ra'}, {'anchor': 'ld'},
            {'anchor': 'rd'}, {'anchor': 'lm'}, {'anchor': 'rm'},
            {'anchor': 'ma'}, {'anchor': 'md'}, {'anchor': 'mm'},
        ]

        for x in range(3):
            for y in range(3):
                w = (self.spines.width - self.horizontal_offset * 1.5)
                h = (self.spines.height - self.vertical_offset * 1.5)

                ow = self.spines.horizontal_offset + self.horizontal_offset * 0.75
                oh = self.spines.vertical_offset + self.vertical_offset * 0.75

                coords = Coords(
                    x0 = ow + w / 3 * x,
                    y0 = oh + h / 3 * y,
                    x1 = ow + w / 3 * (x + 1),
                    y1 = oh + h / 3 * (y + 1)
                )

                point = Point(
                    x = ow + w / 2 * x,
                    y = oh + h / 2 * y
                )

                sections[priority[f'{x}{y}']]['bbox'] = coords
                sections[priority[f'{x}{y}']]['point'] = point

        pts = [self.get_axes_points_coords(ax) for ax in axes]
        points = np.concatenate(pts)

        for p in points:
            point = Point(p[0], p[1])
            for sk, sv in enumerate(sections):
                if 'hits' not in sections[sk]:
                    sections[sk]['hits'] = 0
                if _point_in_bbox(point, sv['bbox']):
                    sections[sk]['hits'] += 1

        section = sorted(sections, key=lambda d: d['hits'])[0]
        return section

#-------------------------------------------------------------------------------
