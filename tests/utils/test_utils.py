# -*- coding: utf-8 -*-

from simpleplots.utils import get_text_dimensions, frange, scale_range, smartrange
import unittest

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

    def test_frange_without_step(self):
        to_test = list(frange(0.1, 0.2))
        expected = [0.1, 0.2]
        self.assertListEqual(to_test, expected)

    def test_frange_with_step(self):
        to_test = list(frange(0.1, 0.2, 0.01))
        expected = [0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2]
        self.assertListEqual(to_test, expected)

    def test_frange_negative_numbers(self):
        to_test = list(frange(-0.9, -0.1))
        expected = [-0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1]
        self.assertListEqual(to_test, expected)

    def test_frange_negative_and_positive_numbers(self):
        to_test = list(frange(-0.9, 0.2))
        expected = [-0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2]
        self.assertListEqual(to_test, expected)

    def test_smartrange_floats_without_gaps(self):
        to_test = list(smartrange(0.1, 0.2, [0.1, 0.2]))
        expected = [0.1, 0.2]
        self.assertListEqual(to_test, expected)

    def test_smartrange_floats_with_gaps(self):
        to_test = list(smartrange(0.1, 0.4, [0.1, 0.2, 0.3]))
        expected = [0.1, 0.2, 0.3, 0.4]
        self.assertListEqual(to_test, expected)

    def test_smartrange_integers_without_gaps(self):
        to_test = list(smartrange(1, 2, [1, 2]))
        expected = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
        self.assertListEqual(to_test, expected)

    def test_smartrange_integers_with_gaps(self):
        to_test = list(smartrange(1, 20, list(range(1, 21))))
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        self.assertListEqual(to_test, expected)

#-----------------------------------------------------------------------------
