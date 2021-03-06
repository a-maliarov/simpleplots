# -*- coding: utf-8 -*-

from simpleplots.utils import get_text_dimensions, smartrange, frange
import unittest
import numpy as np

#-----------------------------------------------------------------------------

class TestUtils(unittest.TestCase):

    def test_get_text_dimensions(self):
        pass

    def test_frange_without_step(self):
        to_test = list(frange(0.1, 0.6))
        expected = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        self.assertListEqual(to_test, expected)

    def test_smartrange_floats_without_gaps(self):
        ov = np.asarray([0.1, 0.2])
        to_test = smartrange(0.1, 0.2, ov).tolist()
        expected = np.asarray([0.1, 0.2]).tolist()
        self.assertListEqual(to_test, expected)

    def test_smartrange_floats_with_gaps(self):
        ov = np.asarray([0.1, 0.2, 0.3])
        to_test = smartrange(0.1, 0.4, ov).tolist()
        expected = np.asarray([0.1, 0.2, 0.3, 0.4]).tolist()
        self.assertListEqual(to_test, expected)

    def test_smartrange_integers_without_gaps(self):
        ov = np.asarray([1, 2])
        to_test = smartrange(1, 2, ov).tolist()
        expected = np.asarray([1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]).tolist()
        self.assertListEqual(to_test, expected)

    def test_smartrange_integers_with_gaps(self):
        ov = np.asarray(list(range(1, 21)))
        to_test = smartrange(1, 20, ov).tolist()
        expected = np.asarray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]).tolist()
        self.assertListEqual(to_test, expected)

#-----------------------------------------------------------------------------
