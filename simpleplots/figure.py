# -*- coding: utf-8 -*-

"""
simpleplots.figure
~~~~~~~~~~~~~~~~~~

This module contains Figure instance.

"""

from .base import Tuple, Theme, Axes, Coords
from .utils import get_text_dimensions, smartrange
from .visuals import Spines, PointsGrid
from .themes import StandardTheme
from .ticker import MaxNLocator

from PIL import Image, ImageDraw, ImageFont
import os

#-------------------------------------------------------------------------------

class Figure(object):

    def __init__(self, size: Tuple[int, int] = (1600, 1200),
                 theme: Theme = StandardTheme) -> None:
        """
        Initializes the Figure instance responsible for all the operations
        on visualizing plots:

            fig = Figure()
            fig.plot([2, 3, 4], [4, 2, 3], color='red', linewidth=7)
            fig.show()

        Supports creation of multiple plots within one figure:

            fig = Figure()
            fig.plot([2, 3, 4], [1, 4.3, 6], color='red', linewidth=7)
            fig.plot([1, 3.5, 7], [2, 3, 5], color='blue', linewidth=7)
            fig.show()

        It is recommended to explicitly close the figure:

            ...
            fig.close()

        """

        self.width = size[0] * 2
        self.height = size[1] * 2
        self.theme = theme

        package_directory_path = os.path.abspath(os.path.dirname(__file__))
        self.fonts_folder = os.path.join(package_directory_path, 'fonts')

        self.img = None
        self.draw = None

        self.spines = Spines(self.width, self.height, self.theme)
        self.grid = PointsGrid(self.spines, self.theme)
        self.locator = MaxNLocator()

        self.axes = list()

        self.tick_length = self.width * self.theme.tick_length_perc
        self.tick_font = ImageFont.truetype(
            os.path.join(self.fonts_folder, self.theme.tick_label_font),
            int(self.width * self.theme.tick_label_size_perc)
        )

    def _create_empty_image(self, _mode: str = 'RGB') -> None:
        if self.img:
            self.img.close()

        self.img = Image.new(_mode, (self.width, self.height),
            color=self.theme.figure_background_color)
        self.draw = ImageDraw.Draw(self.img)

    def _draw_spines(self) -> None:
        for spine in self.spines.all:
            self.draw.line(
                spine,
                fill=self.theme.spine_color,
                width=self.theme.spine_width
            )

    def _set_grid_values(self) -> None:
        xvalues = list()
        for axes in self.axes:
            xvalues.extend(axes.xvalues)
        x_major_ticks = self.locator.tick_values(min(xvalues), max(xvalues))
        # print(x_major_ticks)

        yvalues = list()
        for axes in self.axes:
            yvalues.extend(axes.yvalues)
        y_major_ticks = self.locator.tick_values(min(yvalues), max(yvalues))
        # print(y_major_ticks)

        display_xvmin, display_xvmax = min(x_major_ticks), max(x_major_ticks)
        self.grid.xvalues = smartrange(display_xvmin, display_xvmax, xvalues)
        self.grid.x_major_ticks = x_major_ticks

        display_yvmin, display_yvmax = min(y_major_ticks), max(y_major_ticks)
        self.grid.yvalues = smartrange(display_yvmin, display_yvmax, yvalues)
        self.grid.y_major_ticks = y_major_ticks

    def _draw_grid(self) -> None:
        for column, x_value in enumerate(self.grid.xvalues):
            if not x_value in self.grid.x_major_ticks:
                continue

            grid_vertical_line_coords = Coords(
                self.spines.horizontal_offset + self.grid.horizontal_offset + self.grid.cell_width * column,
                self.spines.vertical_offset,
                self.spines.horizontal_offset + self.grid.horizontal_offset + self.grid.cell_width * column,
                self.spines.vertical_offset + self.grid.vertical_offset * 2 + self.grid.cell_height * (len(self.grid.yvalues) - 1)
            )

            self.draw.line(
                grid_vertical_line_coords,
                fill=self.theme.grid_line_color,
                width=self.theme.grid_line_width
            )

        for row, y_value in enumerate(reversed(self.grid.yvalues)):
            if not y_value in self.grid.y_major_ticks:
                continue

            grid_horizontal_line_coords = Coords(
                self.spines.horizontal_offset,
                self.spines.vertical_offset + self.grid.vertical_offset + self.grid.cell_height * row,
                self.spines.horizontal_offset + self.grid.horizontal_offset * 2 + self.grid.cell_width * (len(self.grid.xvalues) - 1),
                self.spines.vertical_offset + self.grid.vertical_offset + self.grid.cell_height * row
            )

            self.draw.line(
                grid_horizontal_line_coords,
                fill=self.theme.grid_line_color,
                width=self.theme.grid_line_width
            )

    def _draw_ticks(self) -> None:
        for column, x_value in enumerate(self.grid.xvalues):
            if not x_value in self.grid.x_major_ticks:
                continue

            grid_vertical_tick_coords = Coords(
                self.spines.horizontal_offset + self.grid.horizontal_offset + self.grid.cell_width * column,
                self.spines.vertical_offset + self.grid.vertical_offset * 2 + self.grid.cell_height * (len(self.grid.yvalues) - 1),
                self.spines.horizontal_offset + self.grid.horizontal_offset + self.grid.cell_width * column,
                self.spines.vertical_offset + self.grid.vertical_offset * 2 + self.grid.cell_height * (len(self.grid.yvalues) - 1) + self.tick_length
            )

            self.draw.line(
                grid_vertical_tick_coords,
                fill=self.theme.tick_line_color,
                width=self.theme.tick_line_width
            )

        for row, y_value in enumerate(reversed(self.grid.yvalues)):
            if not y_value in self.grid.y_major_ticks:
                continue

            grid_horizontal_tick_coords = Coords(
                self.spines.horizontal_offset - self.tick_length,
                self.spines.vertical_offset + self.grid.vertical_offset + self.grid.cell_height * row,
                self.spines.horizontal_offset,
                self.spines.vertical_offset + self.grid.vertical_offset + self.grid.cell_height * row
            )

            self.draw.line(
                grid_horizontal_tick_coords,
                fill=self.theme.tick_line_color,
                width=self.theme.tick_line_width
            )

    def _draw_tick_labels(self) -> None:
        for column, x_value in enumerate(self.grid.xvalues):
            if not x_value in self.grid.x_major_ticks:
                continue

            text = str(x_value)
            text_width, text_height = get_text_dimensions(text, self.tick_font)

            text_coords = (
                self.spines.horizontal_offset + self.grid.horizontal_offset + self.grid.cell_width * column,
                self.spines.vertical_offset + self.grid.vertical_offset * 2 + self.grid.cell_height * (len(self.grid.yvalues) - 1) + self.tick_length * 2 + text_height / 2,
            )

            self.draw.text(
                text_coords,
                text=text,
                fill=self.theme.tick_label_color,
                font=self.tick_font,
                anchor="mm"
            )

        for row, y_value in enumerate(reversed(self.grid.yvalues)):
            if not y_value in self.grid.y_major_ticks:
                continue

            text = str(y_value)
            text_width, text_height = get_text_dimensions(text, self.tick_font)

            text_coords = (
                self.spines.horizontal_offset - self.tick_length * 2 - text_width / 2,
                self.spines.vertical_offset + self.grid.vertical_offset + self.grid.cell_height * row,
            )

            self.draw.text(
                text_coords,
                text=text,
                fill=self.theme.tick_label_color,
                font=self.tick_font,
                anchor="mm"
            )

    def _identify_and_draw_points(self, xvalues: list, yvalues: list, color: str) -> list:
        viable_points = list()
        for x, y in zip(xvalues, yvalues):
            x_coordinate = [i for i in self.grid.x_connections if i['point_value'] == x][0]['point_coords']
            y_coordinate = [i for i in self.grid.y_connections if i['point_value'] == y][0]['point_coords']
            point_coords = (x_coordinate, y_coordinate)

            viable_points.append(point_coords)
            self.draw.ellipse(
                (
                    point_coords[0] - self.theme.point_radius,
                    point_coords[1] - self.theme.point_radius,
                    point_coords[0] + self.theme.point_radius,
                    point_coords[1] + self.theme.point_radius
                ),
                fill=color
            )

        return viable_points

    def _draw_lines_between_points(self, points: list, color: str, linewidth: int) -> None:
        for point_index, point in enumerate(points):
            if len(points) == point_index + 1:
                break

            first_point_coords = point
            second_point_coords = points[point_index + 1]

            connection_line_coords = (*first_point_coords, *second_point_coords)
            self.draw.line(connection_line_coords, fill=color, width=linewidth)

    def title(self, text):
        title_font = ImageFont.truetype(
            os.path.join(self.fonts_folder, self.theme.title_font),
            int(self.width * self.theme.title_size_perc)
        )

        text_width, text_height = get_text_dimensions(text, title_font)

        text_coords = (
            self.width / 2,
            self.spines.vertical_offset - self.tick_length * 2 - text_height / 2,
        )

        self.draw.text(text_coords, text, fill=self.theme.title_color, font=title_font, anchor="mm")

    def plot(self, xvalues, yvalues, color='red', linewidth=4):
        self._create_empty_image()
        self._draw_spines()

        axes = Axes(xvalues, yvalues, color, linewidth)
        self.axes.append(axes)

        self._set_grid_values()
        self.grid.configure_size()
        self.grid.map_values_with_coords()

        if self.theme.grid_visibility:
            self._draw_grid()

        self._draw_ticks()
        self._draw_tick_labels()

        for axes in self.axes:
            viable_points = self._identify_and_draw_points(axes.xvalues, axes.yvalues, axes.color)
            self._draw_lines_between_points(viable_points, axes.color, axes.linewidth)

    def show(self) -> None:
        self.img = self.img.resize((self.width // 2, self.height // 2), resample=Image.ANTIALIAS)
        self.img.show()

    def close(self):
        self.img.close()

#-------------------------------------------------------------------------------
