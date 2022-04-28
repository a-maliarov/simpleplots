# -*- coding: utf-8 -*-

from simpleplots import Figure
from simpleplots.dates import (YearLocator, YearLocator, MonthLocator,
                               WeekdayLocator, DayLocator, HourLocator,
                               MinuteLocator, SecondLocator, DateFormatter)
import platform
import unittest
import numpy as np
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

        expected = [36.0, 18.9]
        self.assertListEqual(expected, to_test)

    def test_plot_integers_with_gaps(self):
        fig = Figure(size=(500, 300))
        fig.plot([2, 3, 6], [1, 2, 10], color='red', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [18.0, 42.0]
        self.assertListEqual(expected, to_test)

    def test_plot_large_integers_list(self):
        fig = Figure(size=(500, 300))
        fig.plot(list([i for i in range(1, 50000)]), list([i for i in range(1, 50000)]), color='red', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [0.144, 0.0756]
        self.assertListEqual(expected, to_test)

    def test_plot_floats_without_gaps(self):
        fig = Figure(size=(500, 300))
        fig.plot([0.1, 0.2, 0.3], [0.7, 0.8, 0.9], color='red', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [360.0, 15.75]
        self.assertListEqual(expected, to_test)

    def test_plot_floats_with_gaps(self):
        fig = Figure(size=(500, 300))
        fig.plot([0.1, 0.2, 3.5], [0.7, 1.8, 2.4], color='red', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [20.0, 21.0]
        self.assertListEqual(expected, to_test)

    def test_plot_small_floats_small_list(self):
        fig = Figure(size=(500, 300))
        fig.plot([0.000001, 0.000002], [0.000007, 0.000008], color='red', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [720.0, 378.0]
        self.assertListEqual(expected, to_test)

    def test_plot_small_floats_large_list(self):
        fig = Figure(size=(500, 300))
        fig.plot([0.000001, 1], [0.000007, 1], color='red', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [72.0, 37.8]
        self.assertListEqual(expected, to_test)

    def test_multiple_plots(self):
        fig = Figure(size=(500, 300))
        fig.plot([1, 2, 3], [1, 2, 3], color='red', linewidth=7)
        fig.plot([4, 5, 6], [4, 5, 6], color='blue', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [144.0, 75.6]
        self.assertListEqual(expected, to_test)

    def test_single_point_plot(self):
        fig = Figure(size=(500, 300))
        fig.plot([1], [3], color='red', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [720.0, 378.0]
        self.assertListEqual(expected, to_test)

    def test_plot_dates_without_gaps(self):
        dmin = np.datetime64('2022-01')
        dmax = np.datetime64('2022-05')
        delta = np.timedelta64(1, 'M')
        times = np.arange(dmin, dmax, delta)
        y = list(range(len(times)))

        fig = Figure(size=(500, 300))
        fig.plot(times, y, color='red', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [8.0, 11.8125]
        self.assertListEqual(expected, to_test)

    def test_plot_dates_with_gaps(self):
        dmin = np.datetime64('2022-01')
        dmax = np.datetime64('2022-05')
        delta = np.timedelta64(1, 'M')
        times1 = np.arange(dmin, dmax, delta)

        dmin = np.datetime64('2022-08-01')
        dmax = np.datetime64('2022-08-30')
        delta = np.timedelta64(1, 'D')
        times2 = np.arange(dmin, dmax, delta)

        times = np.concatenate([times1, times2])
        y = list(range(len(times)))

        fig = Figure(size=(500, 300))
        fig.plot(times, y, color='red', linewidth=7)
        to_test = [fig.grid.cell_width, fig.grid.cell_height]
        fig.close()

        expected = [3.0, 11.8125]
        self.assertListEqual(expected, to_test)

    def test_plot_dates_with_year_locator(self):
        dmin = np.datetime64('2022')
        dmax = np.datetime64('2030')
        delta = np.timedelta64(1, 'Y')
        times = np.arange(dmin, dmax, delta)
        y = list(range(len(times)))

        fig = Figure(size=(500, 300))
        locator = YearLocator()
        fig.set_major_locator(locator, axis='x')

        fig.plot(times, y, color='red', linewidth=7)
        to_test = [round(fig.grid.cell_width, 2), fig.grid.cell_height]
        fig.close()

        expected = [0.28, 54.0]
        self.assertListEqual(expected, to_test)

    def test_plot_dates_with_month_locator(self):
        dmin = np.datetime64('2022-01')
        dmax = np.datetime64('2022-12')
        delta = np.timedelta64(1, 'M')
        times = np.arange(dmin, dmax, delta)
        y = list(range(len(times)))

        fig = Figure(size=(500, 300))
        locator = MonthLocator()
        fig.set_major_locator(locator, axis='x')

        fig.plot(times, y, color='red', linewidth=7)
        to_test = [round(fig.grid.cell_width, 2), fig.grid.cell_height]
        fig.close()

        expected = [2.37, 37.8]
        self.assertListEqual(expected, to_test)

    def test_plot_dates_with_day_locator(self):
        dmin = np.datetime64('2022-01-01')
        dmax = np.datetime64('2022-01-25')
        delta = np.timedelta64(1, 'D')
        times = np.arange(dmin, dmax, delta)
        y = list(range(len(times)))

        fig = Figure(size=(500, 300))
        locator = DayLocator()
        fig.set_major_locator(locator, axis='x')

        fig.plot(times, y, color='red', linewidth=7)
        to_test = [round(fig.grid.cell_width, 2), fig.grid.cell_height]
        fig.close()

        expected = [1.3, 15.75]
        self.assertListEqual(expected, to_test)

    def test_plot_dates_with_hour_locator(self):
        dmin = np.datetime64('2022-01-01 01')
        dmax = np.datetime64('2022-01-01 15')
        delta = np.timedelta64(1, 'h')
        times = np.arange(dmin, dmax, delta)
        y = list(range(len(times)))

        fig = Figure(size=(500, 300))
        locator = HourLocator()
        fig.set_major_locator(locator, axis='x')

        formatter = DateFormatter('%H:%M:%S', rotation=45)
        fig.set_major_formatter(formatter, axis='x')

        fig.plot(times, y, color='red', linewidth=7)
        to_test = [round(fig.grid.cell_width, 2), fig.grid.cell_height]
        fig.close()

        expected = [0.92, 27.0]
        self.assertListEqual(expected, to_test)

    def test_plot_dates_with_minute_locator(self):
        dmin = np.datetime64('2022-01-01 01:01')
        dmax = np.datetime64('2022-01-01 01:10')
        delta = np.timedelta64(1, 'm')
        times = np.arange(dmin, dmax, delta)
        y = list(range(len(times)))

        fig = Figure(size=(500, 300))
        locator = MinuteLocator()
        fig.set_major_locator(locator, axis='x')

        formatter = DateFormatter('%H:%M:%S', rotation=45)
        fig.set_major_formatter(formatter, axis='x')

        fig.plot(times, y, color='red', linewidth=7)
        to_test = [round(fig.grid.cell_width, 2), fig.grid.cell_height]
        fig.close()

        expected = [1.5, 47.25]
        self.assertListEqual(expected, to_test)

    def test_plot_dates_with_second_locator(self):
        dmin = np.datetime64('2022-01-01 01:01:01')
        dmax = np.datetime64('2022-01-01 01:01:17')
        delta = np.timedelta64(1, 's')
        times = np.arange(dmin, dmax, delta)
        y = list(range(len(times)))

        fig = Figure(size=(500, 300))
        locator = SecondLocator()
        fig.set_major_locator(locator, axis='x')

        formatter = DateFormatter('%H:%M:%S', rotation=45)
        fig.set_major_formatter(formatter, axis='x')

        fig.plot(times, y, color='red', linewidth=7)
        to_test = [round(fig.grid.cell_width, 2), fig.grid.cell_height]
        fig.close()

        expected = [48.0, 23.625]
        self.assertListEqual(expected, to_test)

    def test_save(self):
        fig = Figure(size=(500, 300))
        fig.plot([1, 2, 3], [1, 2, 3], color='red', linewidth=7)
        fig.title('Test')
        fig.save(os.path.join(here, 'graph.png'))

        with self.subTest():
            self.assertTrue('graph.png' in os.listdir(here))
        os.remove(os.path.join(here, 'graph.png'))

    @unittest.skipIf(platform.platform().startswith('Windows'), reason='No need')
    def test_show(self):
        # Not a real test
        try:
            fig = Figure(size=(500, 300))
            fig.plot([1, 2, 3], [1, 2, 3], color='red', linewidth=7)
            fig.legend()
            fig.show()
        except:
            pass

        self.assertTrue(True)

#--------------------------------------------------------------------------------------------------------------
