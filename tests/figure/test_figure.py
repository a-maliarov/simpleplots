# -*- coding: utf-8 -*-

from simpleplots import Figure
import unittest
import os

#--------------------------------------------------------------------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))

class TestFigure(unittest.TestCase):

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

    def test_plot_integers_with_gaps(self):
        fig = Figure(size=(500, 300))
        fig.plot([2, 3, 6], [1, 2, 10], color='red', linewidth=7)
        y_to_test = fig.grid.y_connections
        x_to_test = fig.grid.x_connections
        fig.close()

        with self.subTest():
            expected = {1: 516.0, 2: 468.0, 3: 420.0, 4: 372.0, 5: 324.0, 6: 276.0, 7: 228.0, 8: 180.0, 9: 132.0, 10: 84.0}
            self.assertDictEqual(expected, y_to_test)

        with self.subTest():
            expected = {2.0: 141.0, 2.1: 159.0, 2.2: 177.0, 2.3: 195.0, 2.4: 213.0, 2.5: 231.0, 2.6: 249.0, 2.7: 267.0, 2.8: 285.0, 2.9: 303.0, 3.0: 321.0, 3.1: 339.0, 3.2: 357.0, 3.3: 375.0, 3.4: 393.0, 3.5: 411.0, 3.6: 429.0, 3.7: 447.0, 3.8: 465.0, 3.9: 483.0, 4.0: 501.0, 4.1: 519.0, 4.2: 537.0, 4.3: 555.0, 4.4: 573.0, 4.5: 591.0, 4.6: 609.0, 4.7: 627.0, 4.8: 645.0, 4.9: 663.0, 5.0: 681.0, 5.1: 699.0, 5.2: 717.0, 5.3: 735.0, 5.4: 753.0, 5.5: 771.0, 5.6: 789.0, 5.7: 807.0, 5.8: 825.0, 5.9: 843.0, 6.0: 861.0}
            self.assertDictEqual(expected, x_to_test)

    def test_plot_floats_without_gaps(self):
        fig = Figure(size=(500, 300))
        fig.plot([0.1, 0.2, 0.3], [0.7, 0.8, 0.9], color='red', linewidth=7)
        y_to_test = fig.grid.y_connections
        x_to_test = fig.grid.x_connections
        fig.close()

        with self.subTest():
            expected = {0.68: 516.0, 0.69: 498.0, 0.7: 480.0, 0.71: 462.0, 0.72: 444.0, 0.73: 426.0, 0.74: 408.0, 0.75: 390.0, 0.76: 372.0, 0.77: 354.0, 0.78: 336.0, 0.79: 318.0, 0.8: 300.0, 0.81: 282.0, 0.82: 264.0, 0.83: 246.0, 0.84: 228.0, 0.85: 210.0, 0.86: 192.0, 0.87: 174.0, 0.88: 156.0, 0.89: 138.0, 0.9: 120.0, 0.91: 102.0, 0.92: 84.0}
            self.assertDictEqual(expected, y_to_test)

        with self.subTest():
            expected = {0.1: 141.0, 0.2: 501.0, 0.3: 861.0}
            self.assertDictEqual(expected, x_to_test)

    def test_plot_floats_with_gaps(self):
        fig = Figure(size=(500, 300))
        fig.plot([0.1, 0.2, 3.5], [0.7, 1.8, 2.4], color='red', linewidth=7)
        y_to_test = fig.grid.y_connections
        x_to_test = fig.grid.x_connections
        fig.close()

        with self.subTest():
            expected = {0.6: 516.0, 0.7: 492.0, 0.8: 468.0, 0.9: 444.0, 1.0: 420.0, 1.1: 396.0, 1.2: 372.0, 1.3: 348.0, 1.4: 324.0, 1.5: 300.0, 1.6: 276.0, 1.7: 252.0, 1.8: 228.0, 1.9: 204.0, 2.0: 180.0, 2.1: 156.0, 2.2: 132.0, 2.3: 108.0, 2.4: 84.0}
            self.assertDictEqual(expected, y_to_test)

        with self.subTest():
            expected = {0.0: 141.0, 0.1: 161.0, 0.2: 181.0, 0.3: 201.0, 0.4: 221.0, 0.5: 241.0, 0.6: 261.0, 0.7: 281.0, 0.8: 301.0, 0.9: 321.0, 1.0: 341.0, 1.1: 361.0, 1.2: 381.0, 1.3: 401.0, 1.4: 421.0, 1.5: 441.0, 1.6: 461.0, 1.7: 481.0, 1.8: 501.0, 1.9: 521.0, 2.0: 541.0, 2.1: 561.0, 2.2: 581.0, 2.3: 601.0, 2.4: 621.0, 2.5: 641.0, 2.6: 661.0, 2.7: 681.0, 2.8: 701.0, 2.9: 721.0, 3.0: 741.0, 3.1: 761.0, 3.2: 781.0, 3.3: 801.0, 3.4: 821.0, 3.5: 841.0, 3.6: 861.0}
            self.assertDictEqual(expected, x_to_test)

    def test_multiple_plots(self):
        fig = Figure(size=(500, 300))
        fig.plot([1, 2, 3], [1, 2, 3], color='red', linewidth=7)
        fig.plot([4, 5, 6], [4, 5, 6], color='blue', linewidth=7)
        y_to_test = fig.grid.y_connections
        x_to_test = fig.grid.x_connections
        fig.close()

        with self.subTest():
            expected = {1: 516.0, 2: 429.6, 3: 343.20000000000005, 4: 256.8, 5: 170.4, 6: 84.0}
            self.assertDictEqual(expected, y_to_test)

        with self.subTest():
            expected = {1: 141.0, 2: 285.0, 3: 429.0, 4: 573.0, 5: 717.0, 6: 861.0}
            self.assertDictEqual(expected, x_to_test)

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
        fig = Figure(size=(500, 300))
        fig.plot([1, 2, 3], [1, 2, 3], color='red', linewidth=7)
        fig.show()
        fig.close()

        self.assertTrue(True)

#--------------------------------------------------------------------------------------------------------------
