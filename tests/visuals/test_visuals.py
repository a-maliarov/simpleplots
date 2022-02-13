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

    # Add tests for the new methods after 0.4.0

#-----------------------------------------------------------------------------
