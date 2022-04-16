# -*- coding: utf-8 -*-

"""
simpleplots.figure
~~~~~~~~~~~~~~~~~~

This module contains Figure instance.

"""

__all__ = ('Figure')

from .base import Theme, Axes, Size
from .utils import (get_indices_of_values_in_list, smartrange, normalize_values,
                    get_font, choose_locator, choose_formatter)
from .visuals import Spines, PointsGrid, CustomImageDraw
from .themes import StandardTheme
from .ticker import Locator, Formatter

from numpy.typing import ArrayLike

from PIL import Image
import numpy as np
import gc

#-------------------------------------------------------------------------------

class Figure(object):

    def __init__(self, size: Size = (1600, 1200), theme: Theme = StandardTheme):
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

        self.img = None
        self.draw = None
        self.axes = list()

        self.spines = Spines(self.width, self.height, self.theme)
        self.grid = PointsGrid(self.spines, self.theme)

        self.x_locator = None
        self.y_locator = None

        self.x_formatter = None
        self.y_formatter = None

    def _create_empty_image(self, _mode: str = 'RGB') -> None:
        """Creates an empty image and initializes CustomImageDraw."""
        if self.img:
            self.img.close()

        self.img = Image.new(_mode, (self.width, self.height),
                             color=self.theme.figure_background_color)
        self.draw = CustomImageDraw(self.img)

    def _draw_spines(self) -> None:
        """Draws graph spines."""
        for spine in self.spines.all:
            self.draw.line(
                xy=spine,
                fill=self.theme.spine_color,
                width=self.theme.spine_width
            )

    def _configure_locators(self) -> None:
        if not self.x_locator:
            xvalues = np.concatenate([axes.xvalues for axes in self.axes])
            self.x_locator = choose_locator(xvalues)

        if not self.y_locator:
            yvalues = np.concatenate([axes.yvalues for axes in self.axes])
            self.y_locator = choose_locator(yvalues)

    def _configure_formatters(self) -> None:
        if not self.x_formatter:
            xvalues = np.concatenate([axes.xvalues for axes in self.axes])
            self.x_formatter = choose_formatter(xvalues)

        if not self.y_formatter:
            yvalues = np.concatenate([axes.yvalues for axes in self.axes])
            self.y_formatter = choose_formatter(yvalues)

    def _configure_grid_settings(self) -> None:
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

        xvalues = np.concatenate([axes.xvalues for axes in self.axes])
        x_major_ticks = self.x_locator.tick_values(np.min(xvalues), np.max(xvalues))
        xvmin, xvmax = np.min(x_major_ticks), np.max(x_major_ticks)

        self.grid.xvalues = smartrange(xvmin, xvmax, xvalues)
        self.grid.cell_width = self.grid.width / max(len(self.grid.xvalues) - 1, 1)
        self.grid.x_major_ticks = get_indices_of_values_in_list(x_major_ticks,
                                                                self.grid.xvalues)

        #-----------------------------------------------------------------------

        yvalues = np.concatenate([axes.yvalues for axes in self.axes])
        y_major_ticks = self.y_locator.tick_values(np.min(yvalues), np.max(yvalues))
        yvmin, yvmax = np.min(y_major_ticks), np.max(y_major_ticks)

        self.grid.yvalues = smartrange(yvmin, yvmax, yvalues)
        self.grid.cell_height = self.grid.height / max(len(self.grid.yvalues) - 1, 1)
        self.grid.y_major_ticks = get_indices_of_values_in_list(y_major_ticks,
                                                                self.grid.yvalues)

    def _draw_grid(self) -> None:
        """Draws grid lines within spines box."""
        for x_index in self.grid.x_major_ticks:
            line_coords = self.grid.get_x_line_coords(x_index)

            self.draw.line(
                xy=line_coords,
                fill=self.theme.grid_line_color,
                width=self.theme.grid_line_width
            )

        for y_index in self.grid.y_major_ticks:
            line_coords = self.grid.get_y_line_coords(y_index)

            self.draw.line(
                xy=line_coords,
                fill=self.theme.grid_line_color,
                width=self.theme.grid_line_width
            )

    def _draw_major_ticks(self) -> None:
        """Draws ticks along spines box."""
        for x_index in self.grid.x_major_ticks:
            tick_coords = self.grid.get_x_tick_coords(x_index)

            self.draw.line(
                xy=tick_coords,
                fill=self.theme.tick_line_color,
                width=self.theme.tick_line_width
            )

        for y_index in self.grid.y_major_ticks:
            tick_coords = self.grid.get_y_tick_coords(y_index)

            self.draw.line(
                xy=tick_coords,
                fill=self.theme.tick_line_color,
                width=self.theme.tick_line_width
            )

    def _draw_tick_labels(self) -> None:
        """Draws major ticks labels."""
        tick_font = get_font('tick_label', self.theme, self.width)

        for x_index in self.grid.x_major_ticks:
            label = self.x_formatter(self.grid.xvalues[x_index])
            if not label:
                continue

            coords = self.grid.get_x_tick_label_coords(x_index, label, tick_font)

            self.draw.rtext(xy=coords, text=label, font=tick_font,
                            anchor="mm", fill=self.theme.tick_label_color,
                            rotation=self.x_formatter.rotation)

        for y_index in self.grid.y_major_ticks:
            label = self.y_formatter(self.grid.yvalues[y_index])
            if not label:
                continue

            coords = self.grid.get_y_tick_label_coords(y_index, label, tick_font)

            self.draw.rtext(xy=coords, text=label, font=tick_font,
                            anchor="mm", fill=self.theme.tick_label_color,
                            rotation=self.y_formatter.rotation)

    def _draw_axes(self, axes: Axes) -> None:
        """Draw axes points and connection lines."""
        px = get_indices_of_values_in_list(axes.xvalues, self.grid.xvalues)
        py = get_indices_of_values_in_list(axes.yvalues, self.grid.yvalues)

        xy_indices = np.dstack(np.asarray([px, py]))[0]
        points = np.asarray([self.grid.get_point_coords(x, y) for x, y in xy_indices])

        for point in points:
            self.draw.ellipse(
                (
                    point[0] - self.theme.point_radius,
                    point[1] - self.theme.point_radius,
                    point[0] + self.theme.point_radius,
                    point[1] + self.theme.point_radius
                ),
                fill=axes.color
            )

        points = [tuple(p) for p in points]
        self.draw.line(points, width=axes.linewidth, fill=axes.color)

    def set_major_locator(self, locator: Locator, axis: str) -> None:
        if axis == 'x':
            self.x_locator = locator
        elif axis == 'y':
            self.y_locator = locator

    def set_major_formatter(self, formatter: Formatter, axis: str) -> None:
        if axis == 'x':
            self.x_formatter = formatter
        elif axis == 'y':
            self.y_formatter = formatter

    def plot(self, xvalues: ArrayLike, yvalues: ArrayLike, color: str = 'red',
             linewidth: int = 4) -> None:
        """
        Plot y versus x as lines and/or markers on the image. Can be called
        multiple times from the same figure to include several properly scaled
        plots within one figure.

        """

        self._create_empty_image()
        self._draw_spines()

        xvalues = normalize_values(xvalues)
        yvalues = normalize_values(yvalues)

        axes = Axes(xvalues, yvalues, color, linewidth)
        self.axes.append(axes)

        self._configure_locators()
        self._configure_formatters()
        self._configure_grid_settings()

        if self.theme.grid_visibility:
            self._draw_grid()

        self._draw_major_ticks()
        self._draw_tick_labels()

        for axes in self.axes:
            self._draw_axes(axes)

    def show(self) -> None:
        """
        Displays the image. This method is mainly intended for debugging
        purposes. On Unix platforms, this method saves the image to a temporary
        PPM file, and calls the xv utility. On Windows, it saves the image to a
        temporary BMP file, and uses the standard BMP display utility to show it
        (usually Paint).

        """

        self.img.show()

    def save(self, path: str, autoclose: bool = True, resample: int = Image.BILINEAR):
        """Saves the figure as an image by the given path."""
        origin_size = (self.width // 2, self.height // 2)
        self.img = self.img.resize(size=origin_size, resample=resample)
        self.img.save(path, compress_level=1)

        if autoclose:
            self.close()

    def close(self) -> None:
        """Explicitly closes the image."""
        self.img.close()
        gc.collect()

    def title(self, text: str) -> None:
        """
        Sets graph's title using given text string. The position of the title
        is located on top of spines box, in the middle of the grid.

        """

        title_font = get_font('title', self.theme, self.width)
        coords = self.grid.get_title_coords(text, title_font)

        self.draw.text(xy=coords, text=text, font=title_font, anchor="mm",
                       fill=self.theme.title_color)

#-------------------------------------------------------------------------------
