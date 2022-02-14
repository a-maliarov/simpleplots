# -*- coding: utf-8 -*-

from simpleplots import Figure
import unittest
import os

#--------------------------------------------------------------------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))

class TestFigure(unittest.TestCase):

    def test_maxnlocator_value_error_1(self):
        with self.assertRaises(Exception) as context:
            fig = Figure(size=(500, 300))
            fig.plot(['a', 'b'], ['a', 'b'], color='red', linewidth=7)
            fig.close()

    def test_plot_integers_without_gaps(self):
        fig = Figure(size=(500, 300))
        fig.plot([2, 3, 4], [1, 2, 3], color='red', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [36.0, 21.6]
        self.assertListEqual(expected, to_test)

    def test_plot_integers_with_gaps(self):
        fig = Figure(size=(500, 300))
        fig.plot([2, 3, 6], [1, 2, 10], color='red', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [18.0, 48.0]
        self.assertListEqual(expected, to_test)

    def test_plot_large_integers_list(self):
        fig = Figure(size=(500, 300))
        fig.plot(list([i for i in range(1, 50000)]), list([i for i in range(1, 50000)]), color='red', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [0.144, 0.0864]
        self.assertListEqual(expected, to_test)

    def test_plot_floats_without_gaps(self):
        fig = Figure(size=(500, 300))
        fig.plot([0.1, 0.2, 0.3], [0.7, 0.8, 0.9], color='red', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [360.0, 18.0]
        self.assertListEqual(expected, to_test)

    def test_plot_floats_with_gaps(self):
        fig = Figure(size=(500, 300))
        fig.plot([0.1, 0.2, 3.5], [0.7, 1.8, 2.4], color='red', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [20.0, 24.0]
        self.assertListEqual(expected, to_test)

    def test_plot_small_floats_list(self):
        fig = Figure(size=(500, 300))
        fig.plot([0.000001, 0.000002], [0.000007, 0.000008], color='red', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [720.0, 432.0]
        self.assertListEqual(expected, to_test)

    def test_multiple_plots(self):
        fig = Figure(size=(500, 300))
        fig.plot([1, 2, 3], [1, 2, 3], color='red', linewidth=7)
        fig.plot([4, 5, 6], [4, 5, 6], color='blue', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [144.0, 86.4]
        self.assertListEqual(expected, to_test)

    def test_save(self):
        fig = Figure(size=(500, 300))
        fig.plot([1, 2, 3], [1, 2, 3], color='red', linewidth=7)
        fig.title('Test')
        fig.save(os.path.join(here, 'graph.png'))

        with self.subTest():
            self.assertTrue('graph.png' in os.listdir(here))
        os.remove(os.path.join(here, 'graph.png'))

    def test_show(self):
        # Not a real test yet
        try:
            fig = Figure(size=(500, 300))
            fig.plot([1, 2, 3], [1, 2, 3], color='red', linewidth=7)
            fig.show()
            fig.close()
        except:
            pass

        self.assertTrue(True)

#--------------------------------------------------------------------------------------------------------------
