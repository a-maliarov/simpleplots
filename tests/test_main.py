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

class TestSimplePlots(unittest.TestCase):

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
        y_to_test = fig.grid.y_connections
        x_to_test = fig.grid.x_connections
        fig.close()

        with self.subTest():
            expected = {1.0: 516.0, 1.1: 494.40000000000003, 1.2: 472.8, 1.3: 451.20000000000005, 1.4: 429.6, 1.5: 408.0, 1.6: 386.40000000000003, 1.7: 364.8, 1.8: 343.20000000000005, 1.9: 321.6, 2.0: 300.0, 2.1: 278.4, 2.2: 256.8, 2.3: 235.20000000000002, 2.4: 213.60000000000002, 2.5: 192.0, 2.6: 170.4, 2.7: 148.8, 2.8: 127.2, 2.9: 105.6, 3.0: 84.0}
            self.assertDictEqual(expected, y_to_test)

        with self.subTest():
            expected = {2.0: 141.0, 2.1: 177.0, 2.2: 213.0, 2.3: 249.0, 2.4: 285.0, 2.5: 321.0, 2.6: 357.0, 2.7: 393.0, 2.8: 429.0, 2.9: 465.0, 3.0: 501.0, 3.1: 537.0, 3.2: 573.0, 3.3: 609.0, 3.4: 645.0, 3.5: 681.0, 3.6: 717.0, 3.7: 753.0, 3.8: 789.0, 3.9: 825.0, 4.0: 861.0}
            self.assertDictEqual(expected, x_to_test)

    # def test_plot_integers_with_gaps(self):
    #     fig = Figure(size=(500, 300))
    #     fig.plot([2, 3, 6], [1, 2, 10], color='red', linewidth=7)
    #     origin_size = (fig.width // 2, fig.height // 2)
    #     fig.img = fig.img.resize(size=origin_size, resample=Image.ANTIALIAS)
    #     to_test = list(fig.img.getdata())
    #     fig.close()
    #
    #     sample_img = Image.open(os.path.join(graphs_folder, 'integers_with_gaps.png'))
    #     expected = list(sample_img.getdata())
    #     sample_img.close()
    #
    #     self.assertListEqual(expected, to_test)
    #
    # def test_plot_floats_without_gaps(self):
    #     fig = Figure(size=(500, 300))
    #     fig.plot([0.1, 0.2, 0.3], [0.7, 0.8, 0.9], color='red', linewidth=7)
    #     origin_size = (fig.width // 2, fig.height // 2)
    #     fig.img = fig.img.resize(size=origin_size, resample=Image.ANTIALIAS)
    #     to_test = list(fig.img.getdata())
    #     fig.close()
    #
    #     sample_img = Image.open(os.path.join(graphs_folder, 'floats_without_gaps.png'))
    #     expected = list(sample_img.getdata())
    #     sample_img.close()
    #
    #     self.assertListEqual(expected, to_test)
    #
    # def test_plot_floats_with_gaps(self):
    #     fig = Figure(size=(500, 300))
    #     fig.plot([0.1, 0.2, 3.5], [0.7, 1.8, 2.4], color='red', linewidth=7)
    #     origin_size = (fig.width // 2, fig.height // 2)
    #     fig.img = fig.img.resize(size=origin_size, resample=Image.ANTIALIAS)
    #     to_test = list(fig.img.getdata())
    #     fig.close()
    #
    #     sample_img = Image.open(os.path.join(graphs_folder, 'floats_with_gaps.png'))
    #     expected = list(sample_img.getdata())
    #     sample_img.close()
    #
    #     self.assertListEqual(expected, to_test)

#--------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()

#--------------------------------------------------------------------------------------------------------------
