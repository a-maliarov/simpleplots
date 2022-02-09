# -*- coding: utf-8 -*-

"""
simpleplots.themes
~~~~~~~~~~~~~~~~~~

"""

from .base import Theme

#-------------------------------------------------------------------------------

class StandardTheme(Theme):
    figure_background_color = (255, 255, 255)

    spine_box_width_perc = 0.8
    spine_box_height_perc = 0.8
    spine_color = (0, 0, 0)
    spine_width = 4

    grid_box_width_perc = 0.9
    grid_box_height_perc = 0.9
    grid_visibility = True
    grid_line_color = (0, 0, 0)
    grid_line_width = 2

    tick_length_perc = 0.005
    tick_line_color = (0, 0, 0)
    tick_line_width = 3

    tick_label_font = 'arial.ttf'
    tick_label_size_perc = 0.016
    tick_label_color = (0, 0, 0)

    point_radius = 4

    title_font = 'arial.ttf'
    title_size_perc = 0.033
    title_color = (0, 0, 0)
