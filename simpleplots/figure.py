# -*- coding: utf-8 -*-

"""
simpleplots.figure
~~~~~~~~~~~~~~~~~~

This module contains Figure instance.

"""

__all__ = ('Figure')

from .base import Tuple, Theme, Axes, Coords, List, Union, Tuple
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
        """Creates an empty image and initializes ImageDraw."""
        if self.img:
            self.img.close()

        self.img = Image.new(_mode, (self.width, self.height),
                             color=self.theme.figure_background_color)
        self.draw = ImageDraw.Draw(self.img)

    def _draw_spines(self) -> None:
        """Draws graph spines."""
        for spine in self.spines.all:
            self.draw.line(
                spine,
                fill=self.theme.spine_color,
                width=self.theme.spine_width
            )

    def _set_grid_values(self) -> None:
        """
        Fills gaps in input values range, finds major ticks and saves all the
        information to PointsGrid.

        Say, the input values are [1, 3, 4], but drawing only these 3 values in
        a row would ruin the scale because by doing so, we unintentionally show
        that the distance between 1 and 3 is the same as the distance between
        3 and 4, which is, of course, false.

        To avoid this, we firstly fill the gaps by converting the [1, 3, 4] to
        [1, 2, 3, 4]. Now, the grid contains all the values to correctly
        visualize the scale.

        At the same time, if the values are, for example, [1, 4, 46, 98] - the
        list with filled gaps would contain almost 100 elements and labeling
        all of them would be a mess. That's why we find "major ticks", in this
        case: [0, 10, 20, 30, ..., 100]. These are the only values that will be
        labeled along spines, although we still keep track of all 100 to display
        the actual plot.

        """

        xvalues = list()
        for axes in self.axes:
            xvalues.extend(axes.xvalues)
        x_major_ticks = self.locator.tick_values(min(xvalues), max(xvalues))

        yvalues = list()
        for axes in self.axes:
            yvalues.extend(axes.yvalues)
        y_major_ticks = self.locator.tick_values(min(yvalues), max(yvalues))

        display_xvmin, display_xvmax = min(x_major_ticks), max(x_major_ticks)
        self.grid.xvalues = smartrange(display_xvmin, display_xvmax, xvalues)
        self.grid.x_major_ticks = x_major_ticks

        display_yvmin, display_yvmax = min(y_major_ticks), max(y_major_ticks)
        self.grid.yvalues = smartrange(display_yvmin, display_yvmax, yvalues)
        self.grid.y_major_ticks = y_major_ticks

    def _draw_grid(self) -> None:
        """Draws grid lines within spines box."""
        for column, x_value in enumerate(self.grid.xvalues):
            if not x_value in self.grid.x_major_ticks:
                continue

            grid_vertical_line_coords = Coords(
                self.spines.horizontal_offset + self.grid.horizontal_offset \
                                              + self.grid.cell_width * column,
                self.spines.vertical_offset,
                self.spines.horizontal_offset + self.grid.horizontal_offset \
                                              + self.grid.cell_width * column,
                self.spines.vertical_offset + self.grid.vertical_offset * 2 \
                                            + self.grid.height
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
                self.spines.vertical_offset + self.grid.vertical_offset \
                                            + self.grid.cell_height * row,
                self.spines.horizontal_offset + self.grid.horizontal_offset * 2 \
                                              + self.grid.width,
                self.spines.vertical_offset + self.grid.vertical_offset
                                            + self.grid.cell_height * row \
            )

            self.draw.line(
                grid_horizontal_line_coords,
                fill=self.theme.grid_line_color,
                width=self.theme.grid_line_width
            )

    def _draw_ticks(self) -> None:
        """Draws ticks along spines box."""
        for column, x_value in enumerate(self.grid.xvalues):
            if not x_value in self.grid.x_major_ticks:
                continue

            grid_vertical_tick_coords = Coords(
                self.spines.horizontal_offset + self.grid.horizontal_offset \
                                              + self.grid.cell_width * column,
                self.spines.vertical_offset + self.grid.vertical_offset * 2 \
                                            + self.grid.height,
                self.spines.horizontal_offset + self.grid.horizontal_offset \
                                              + self.grid.cell_width * column,
                self.spines.vertical_offset + self.grid.vertical_offset * 2 \
                                            + self.grid.height + self.tick_length
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
                self.spines.vertical_offset + self.grid.vertical_offset \
                                            + self.grid.cell_height * row,
                self.spines.horizontal_offset,
                self.spines.vertical_offset + self.grid.vertical_offset \
                                            + self.grid.cell_height * row
            )

            self.draw.line(
                grid_horizontal_tick_coords,
                fill=self.theme.tick_line_color,
                width=self.theme.tick_line_width
            )

    def _draw_tick_labels(self) -> None:
        """Draws major ticks labels."""
        for column, x_value in enumerate(self.grid.xvalues):
            if not x_value in self.grid.x_major_ticks:
                continue

            text = str(x_value)
            text_width, text_height = get_text_dimensions(text, self.tick_font)

            text_coords = (
                self.spines.horizontal_offset + self.grid.horizontal_offset \
                                              + self.grid.cell_width * column,
                self.spines.vertical_offset + self.grid.vertical_offset * 2 \
                                            + self.grid.height              \
                                            + self.tick_length * 2          \
                                            + text_height / 2,
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
                self.spines.horizontal_offset - self.tick_length * 2 \
                                              - text_width / 2,
                self.spines.vertical_offset + self.grid.vertical_offset \
                                            + self.grid.cell_height * row,
            )

            self.draw.text(
                text_coords,
                text=text,
                fill=self.theme.tick_label_color,
                font=self.tick_font,
                anchor="mm"
            )

    def _find_axes_points(self, xvalues: List[Union[int, float]],
                          yvalues: List[Union[int, float]]) -> List[Tuple[int, int]]:
        """
        Create a list of axes points coordinates.

        """

        points = list()
        for x, y in zip(xvalues, yvalues):
            x_coordinate = self.grid.x_connections[x]
            y_coordinate = self.grid.y_connections[y]
            point_coords = (x_coordinate, y_coordinate)

            points.append(point_coords)

        return points

    def _draw_axes(self, points: List[Tuple[int, int]], color: str,
                   linewidth: int) -> None:
        """
        Using axes points coordinates draws points and lines on the image.

        """

        for point_index, point in enumerate(points):
            self.draw.ellipse(
                (
                    point[0] - self.theme.point_radius,
                    point[1] - self.theme.point_radius,
                    point[0] + self.theme.point_radius,
                    point[1] + self.theme.point_radius
                ),
                fill=color
            )

            if len(points) == point_index + 1:
                break

            first_point_coords = point
            second_point_coords = points[point_index + 1]

            connection_line_coords = (*first_point_coords, *second_point_coords)
            self.draw.line(connection_line_coords, fill=color, width=linewidth)

    def title(self, text: str) -> None:
        """
        Sets graph's title using given text string. The location of the title
        is located on top of spines box, in the middle of the image.

        """

        title_font = ImageFont.truetype(
            os.path.join(self.fonts_folder, self.theme.title_font),
            int(self.width * self.theme.title_size_perc)
        )

        text_width, text_height = get_text_dimensions(text, title_font)

        text_coords = (
            self.width / 2,
            self.spines.vertical_offset - self.tick_length * 2 - text_height / 2,
        )

        self.draw.text(
            text_coords,
            text=text,
            fill=self.theme.title_color,
            font=title_font,
            anchor="mm"
        )

    def plot(self, xvalues: List[Union[int, float]], yvalues: List[Union[int, float]],
             color: str = 'red', linewidth: int = 4) -> None:
        """
        Plot y versus x as lines and/or markers on the image. Can be called
        multiple times from the same figure to include several properly scaled
        plots within one figure.

        """

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
            points = self._find_axes_points(axes.xvalues, axes.yvalues)
            self._draw_axes(points, axes.color, axes.linewidth)

    def show(self) -> None:
        """
        Displays the image. This method is mainly intended for debugging
        purposes. On Unix platforms, this method saves the image to a temporary
        PPM file, and calls the xv utility. On Windows, it saves the image to a
        temporary BMP file, and uses the standard BMP display utility to show it
        (usually Paint).
        """

        self.img.show()

    def save(self, path: str, autoclose: bool = True):
        """Saves the figure as an image by the given path."""
        origin_size = (self.width // 2, self.height // 2)
        self.img = self.img.resize(size=origin_size, resample=Image.ANTIALIAS)
        self.img.save(path)

        if autoclose:
            self.close()

    def close(self) -> None:
        """Explicitly closes the image."""
        self.img.close()

#-------------------------------------------------------------------------------
