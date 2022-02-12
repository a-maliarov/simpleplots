# -*- coding: utf-8 -*-

from simpleplots.utils import get_text_dimensions, scale_range, smartrange
import unittest
import numpy as np

#-----------------------------------------------------------------------------

class TestUtils(unittest.TestCase):

    def test_get_text_dimensions(self):
        pass

    def test_scale_range(self):
        scale, offset = scale_range(0.1, 0.3)
        with self.subTest():
            expected = 0.1
            self.assertEqual(scale, expected)

        scale, offset = scale_range(1, 9)
        with self.subTest():
            expected = 1
            self.assertEqual(scale, expected)

        scale, offset = scale_range(1, 20)
        with self.subTest():
            expected = 10
            self.assertEqual(scale, expected)

        scale, offset = scale_range(20, 120)
        with self.subTest():
            expected = 100
            self.assertEqual(scale, expected)

        scale, offset = scale_range(199, 200)
        with self.subTest():
            expected = 100
            self.assertEqual(offset, expected)

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
