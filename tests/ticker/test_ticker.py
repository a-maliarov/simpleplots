# -*- coding: utf-8 -*-

from simpleplots.ticker import MaxNLocator
import unittest

#-----------------------------------------------------------------------------

class TestTicker(unittest.TestCase):

    def test_integers(self):
        loc = MaxNLocator()
        ticks = loc.tick_values(1, 16)
        expected = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0]
        self.assertListEqual(ticks, expected)

    def test_floats(self):
        loc = MaxNLocator()
        ticks = loc.tick_values(0.1, 1.3)
        expected = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4]
        self.assertListEqual(ticks, expected)

#-----------------------------------------------------------------------------
