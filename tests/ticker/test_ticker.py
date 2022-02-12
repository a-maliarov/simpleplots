# -*- coding: utf-8 -*-

from simpleplots.ticker import MaxNLocator, EdgeInteger
import unittest
import numpy as np

#-----------------------------------------------------------------------------

class TestTicker(unittest.TestCase):

    def test_edge_integer_negative_step(self):
        with self.assertRaises(Exception) as context:
            edge = EdgeInteger(-1, 0)

    def test_edge_integer_closeto(self):
        edge = EdgeInteger(1, 1)

        with self.subTest():
            self.assertTrue(edge.closeto(1, 1))

        with self.subTest():
            self.assertFalse(edge.closeto(1, 10))

    def test_maxnlocator_integers(self):
        loc = MaxNLocator()
        ticks = loc.tick_values(1, 16)
        expected = np.asarray([0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0])
        self.assertListEqual(ticks.tolist(), expected.tolist())

    def test_maxnlocator_floats(self):
        loc = MaxNLocator()
        ticks = loc.tick_values(0.1, 1.3)
        expected = np.asarray([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4])
        self.assertListEqual(ticks.tolist(), expected.tolist())

    def test_maxnlocator_floats_reversed(self):
        loc = MaxNLocator()
        ticks = loc.tick_values(1.3, 0.1)
        expected = np.asarray([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4])
        self.assertListEqual(ticks.tolist(), expected.tolist())

    def test_maxnlocator_floats_including_only_integers(self):
        loc = MaxNLocator(integer=True)
        ticks = loc.tick_values(0.1, 2.5)
        expected = np.asarray([0.0, 1.0, 2.0, 3.0])
        self.assertListEqual(ticks.tolist(), expected.tolist())

#-----------------------------------------------------------------------------
