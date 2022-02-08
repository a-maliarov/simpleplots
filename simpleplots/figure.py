# -*- coding: utf-8 -*-

"""
simpleplots.figure
~~~~~~~~~~~~~~~~~~

This module contains Figure instance.

"""

from .base import Tuple, Theme, Axes
from .utils import get_text_dimensions
from .visuals import Spines, PointsGrid
from .themes import StandardTheme

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
            fig.plot([2, 3, 4], [1, 4, 6], color='red', linewidth=7)
            fig.plot([1, 3, 7], [2, 3, 5], color='blue', linewidth=7)
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
        self.grid = PointsGrid(self.spines.width, self.spines.height, self.theme)

        self.axes = list()
        self.x_connections = list()
        self.y_connections = list()

        self.xvalues = list()
        self.yvalues = list()
        # self.xvalues_grid_length = None
        # self.yvalues_grid_length = None
        #
        # self.grid_cell_width = None
        # self.grid_cell_height = None
        # self.grid_horizontal_offset = None
        # self.grid_vertical_offset = None
        #
        # self.float_minor_locator = None
        # self.x_display_rank = None
        # self.x_display_coef = None
        # self.y_display_rank = None
        # self.y_display_coef = None
        #
        # self.tick_length = self.width * self.theme.tick_length_perc
        # self.tick_font = ImageFont.truetype(
        #     os.path.join(self.fonts_folder, self.theme.tick_label_font),
        #     int(self.width * self.theme.tick_label_size_perc)
        # )

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

    def _populate_values(self) -> None:
        xvalues = list()
        for axes in self.axes:
            xvalues.extend(axes.xvalues)

        yvalues = list()
        for axes in self.axes:
            yvalues.extend(axes.yvalues)

        self.xvalues, self.grid.x_lines_number = fill_gaps_and_identify_number_of_grid_lines(xvalues)
        self.yvalues, self.grid.y_lines_number = fill_gaps_and_identify_number_of_grid_lines(yvalues)

    def _to_display(self, value_index, value, axis) -> bool:
        if axis == 'x':
            if value % (self.x_display_rank * self.x_display_coef) == 0:
                return True

        elif axis == 'y':
            if value % (self.y_display_rank * self.y_display_coef) == 0:
                return True

    def _draw_grid(self) -> None:
        for column, x_value in zip(range(self.xvalues_grid_length), self.xvalues_without_gaps):
            if not self._to_display(column, x_value, 'x'):
                continue

            grid_vertical_line_coords = (
                self.spine_box_horizontal_offset + self.grid_horizontal_offset + self.grid_cell_width * column,
                self.spine_box_vertical_offset,
                self.spine_box_horizontal_offset + self.grid_horizontal_offset + self.grid_cell_width * column,
                self.spine_box_vertical_offset + self.grid_vertical_offset * 2 + self.grid_cell_height * (self.yvalues_grid_length - 1)
            )

            self.draw.line(grid_vertical_line_coords, fill=self.theme.grid_line_color, width=self.theme.grid_line_width)

        for row, y_value in zip(range(self.yvalues_grid_length), reversed(self.yvalues_without_gaps)):
            if not self._to_display(row, y_value, 'y'):
                continue

            grid_horizontal_line_coords = (
                self.spine_box_horizontal_offset,
                self.spine_box_vertical_offset + self.grid_vertical_offset + self.grid_cell_height * row,
                self.spine_box_horizontal_offset + self.grid_horizontal_offset * 2 + self.grid_cell_width * (self.xvalues_grid_length - 1),
                self.spine_box_vertical_offset + self.grid_vertical_offset + self.grid_cell_height * row
            )

            self.draw.line(grid_horizontal_line_coords, fill=self.theme.grid_line_color, width=self.theme.grid_line_width)

    def _draw_ticks(self) -> None:
        for column, x_value in zip(range(self.xvalues_grid_length), self.xvalues_without_gaps):
            if not self._to_display(column, x_value, 'x'):
                continue

            grid_vertical_tick_coords = (
                self.spine_box_horizontal_offset + self.grid_horizontal_offset + self.grid_cell_width * column,
                self.spine_box_vertical_offset + self.grid_vertical_offset * 2 + self.grid_cell_height * (self.yvalues_grid_length - 1),
                self.spine_box_horizontal_offset + self.grid_horizontal_offset + self.grid_cell_width * column,
                self.spine_box_vertical_offset + self.grid_vertical_offset * 2 + self.grid_cell_height * (self.yvalues_grid_length - 1) + self.tick_length
            )

            self.draw.line(grid_vertical_tick_coords, fill=self.theme.tick_line_color, width=self.theme.tick_line_width)

        for row, y_value in zip(range(self.yvalues_grid_length), reversed(self.yvalues_without_gaps)):
            if not self._to_display(row, y_value, 'y'):
                continue

            grid_horizontal_tick_coords = (
                self.spine_box_horizontal_offset - self.tick_length,
                self.spine_box_vertical_offset + self.grid_vertical_offset + self.grid_cell_height * row,
                self.spine_box_horizontal_offset,
                self.spine_box_vertical_offset + self.grid_vertical_offset + self.grid_cell_height * row
            )

            self.draw.line(grid_horizontal_tick_coords, fill=self.theme.tick_line_color, width=self.theme.tick_line_width)

    def _draw_tick_labels(self) -> None:
        for column, x_value in zip(range(self.xvalues_grid_length), self.xvalues_without_gaps):
            if not self._to_display(column, x_value, 'x'):
                continue

            text = str(x_value)
            text_width, text_height = get_text_dimensions(text, self.tick_font)

            text_coords = (
                self.spine_box_horizontal_offset + self.grid_horizontal_offset + self.grid_cell_width * column,
                self.spine_box_vertical_offset + self.grid_vertical_offset * 2 + self.grid_cell_height * (self.yvalues_grid_length - 1) + self.tick_length * 2 + text_height / 2,
            )

            self.draw.text(text_coords, text, fill=self.theme.tick_label_color, font=self.tick_font, anchor="mm")

        for row, y_value in zip(range(self.yvalues_grid_length), reversed(self.yvalues_without_gaps)):
            if not self._to_display(row, y_value, 'y'):
                continue

            text = str(y_value)
            text_width, text_height = get_text_dimensions(text, self.tick_font)

            text_coords = (
                self.spine_box_horizontal_offset - self.tick_length * 2 - text_width / 2,
                self.spine_box_vertical_offset + self.grid_vertical_offset + self.grid_cell_height * row,
            )

            self.draw.text(text_coords, text, fill=self.theme.tick_label_color, font=self.tick_font, anchor="mm")

    def _create_value_coordinate_connections(self) -> list:
        self.x_connections = list()
        for x_index, x_value in enumerate(self.xvalues_without_gaps):
            x_coordinate = self.spine_box_horizontal_offset + self.grid_horizontal_offset + (self.grid_cell_width * x_index + 1)

            point_data = {
                'point_value': x_value,
                'point_coords': x_coordinate
            }
            self.x_connections.append(point_data)

        self.y_connections = list()
        for y_index, y_value in enumerate(self.yvalues_without_gaps):
            y_coordinate = self.spine_box_vertical_offset + self.grid_vertical_offset + (self.grid_cell_height * (self.yvalues_grid_length - y_index - 1))

            point_data = {
                'point_value': y_value,
                'point_coords': y_coordinate
            }
            self.y_connections.append(point_data)

    def _identify_and_draw_points(self, xvalues: list, yvalues: list, color: str) -> list:
        viable_points = list()
        for x, y in zip(xvalues, yvalues):
            x_coordinate = [i for i in self.x_connections if i['point_value'] == x][0]['point_coords']
            y_coordinate = [i for i in self.y_connections if i['point_value'] == y][0]['point_coords']
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
            self.spine_box_vertical_offset - self.tick_length * 2 - text_height / 2,
        )

        self.draw.text(text_coords, text, fill=self.theme.title_color, font=title_font, anchor="mm")

    def plot(self, xvalues, yvalues, color='red', linewidth=4):
        self._create_empty_image()
        self._draw_spines()

        axes = Axes(xvalues, yvalues, color, linewidth)
        self.axes.append(axes)
        self._populate_values()

        print(self.xvalues, self.grid.x_lines_number)
        print(self.yvalues, self.grid.y_lines_number)
        # self._set_grid_size()
        # self._set_major_ticks()
        #
        # if self.theme.grid_visibility:
        #     self._draw_grid()
        #
        # self._draw_ticks()
        # self._draw_tick_labels()
        #
        # self._create_value_coordinate_connections()
        #
        # for axes in self.axes:
        #     viable_points = self._identify_and_draw_points(axes.xvalues, axes.yvalues, axes.color)
        #     self._draw_lines_between_points(viable_points, axes.color, axes.linewidth)

    def show(self) -> None:
        self.img = self.img.resize((self.width // 2, self.height // 2), resample=Image.ANTIALIAS)
        self.img.show()

    def close(self):
        self.img.close()

#-------------------------------------------------------------------------------
