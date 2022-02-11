# -*- coding: utf-8 -*-

from simpleplots import Figure
from simpleplots.ticker import MaxNLocator
from PIL import Image
import unittest
import sys
import os

#--------------------------------------------------------------------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))
graphs_folder = os.path.join(here, 'graphs')

class TestAmazonCaptcha(unittest.TestCase):

    def test_ticker_with_integer_input(self):
        loc = MaxNLocator()
        expected = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0, 16.0]
        ticks = loc.tick_values(1, 16)
        self.assertListEqual(expected, ticks)

    def test_ticker_with_float_input(self):
        loc = MaxNLocator()
        expected = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6]
        ticks = loc.tick_values(0.5, 3.4)
        self.assertListEqual(expected, ticks)

    def test_plot_integers_without_gaps(self):
        fig = Figure(size=(500, 300))
        fig.plot([2, 3, 4], [1, 2, 3], color='red', linewidth=7)
        origin_size = (fig.width // 2, fig.height // 2)
        fig.img = fig.img.resize(size=origin_size, resample=Image.ANTIALIAS)
        to_test = list(fig.img.getdata())
        fig.close()

        sample_img = Image.open(os.path.join(graphs_folder, 'integers_without_gaps.png'))
        expected = list(sample_img.getdata())
        sample_img.close()

        self.assertListEqual(expected, to_test)

    def test_plot_integers_with_gaps(self):
        fig = Figure(size=(500, 300))
        fig.plot([2, 3, 6], [1, 2, 10], color='red', linewidth=7)
        origin_size = (fig.width // 2, fig.height // 2)
        fig.img = fig.img.resize(size=origin_size, resample=Image.ANTIALIAS)
        to_test = list(fig.img.getdata())
        fig.close()

        sample_img = Image.open(os.path.join(graphs_folder, 'integers_with_gaps.png'))
        expected = list(sample_img.getdata())
        sample_img.close()

        self.assertListEqual(expected, to_test)

    def test_plot_floats_without_gaps(self):
        fig = Figure(size=(500, 300))
        fig.plot([0.1, 0.2, 0.3], [0.7, 0.8, 0.9], color='red', linewidth=7)
        origin_size = (fig.width // 2, fig.height // 2)
        fig.img = fig.img.resize(size=origin_size, resample=Image.ANTIALIAS)
        to_test = list(fig.img.getdata())
        fig.close()

        sample_img = Image.open(os.path.join(graphs_folder, 'floats_without_gaps.png'))
        expected = list(sample_img.getdata())
        sample_img.close()

        self.assertListEqual(expected, to_test)

    def test_plot_floats_with_gaps(self):
        fig = Figure(size=(500, 300))
        fig.plot([0.1, 0.2, 3.5], [0.7, 1.8, 2.4], color='red', linewidth=7)
        origin_size = (fig.width // 2, fig.height // 2)
        fig.img = fig.img.resize(size=origin_size, resample=Image.ANTIALIAS)
        to_test = list(fig.img.getdata())
        fig.close()

        sample_img = Image.open(os.path.join(graphs_folder, 'floats_with_gaps.png'))
        expected = list(sample_img.getdata())
        sample_img.close()

        self.assertListEqual(expected, to_test)

#--------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

#--------------------------------------------------------------------------------------------------------------
