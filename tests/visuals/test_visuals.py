# -*- coding: utf-8 -*-

from simpleplots.visuals import Spines, PointsGrid
from simpleplots.base import Theme
import unittest

class TestTheme(Theme):
    spine_box_width_perc = 0.8
    spine_box_height_perc = 0.8
    grid_box_width_perc = 0.9
    grid_box_height_perc = 0.9
    tick_length_perc = 0.0075

#-----------------------------------------------------------------------------

class TestVisuals(unittest.TestCase):
    spines = Spines(100, 100, TestTheme)
    grid = PointsGrid(spines, TestTheme)

    def test_spines(self):
        to_test = [tuple(i) for i in self.spines.all]

        expected = [
            (10.0, 10.0, 10.0, 90.0),
            (10.0, 10.0, 90.0, 10.0),
            (90.0, 10.0, 90.0, 90.0),
            (10.0, 90.0, 90.0, 90.0)
        ]
        self.assertListEqual(to_test, expected)

    def test_pointsgrid_configure_size(self):
        self.grid.xvalues = [1, 2, 3, 4]
        self.grid.yvalues = [1, 2, 3, 4]
        self.grid.configure_size()

        to_test = [self.grid.cell_width, self.grid.cell_height]
        expected = [24.0, 24.0]

        self.assertListEqual(to_test, expected)

    def test_pointsgrid_map_values_with_coords(self):
        self.grid.map_values_with_coords()

        with self.subTest():
            expected = {1: 15.0, 2: 39.0, 3: 63.0, 4: 87.0}
            self.assertDictEqual(self.grid.x_connections, expected)

        with self.subTest():
            expected = {1: 86.0, 2: 62.0, 3: 38.0, 4: 14.0}
            self.assertDictEqual(self.grid.y_connections, expected)

#-----------------------------------------------------------------------------
