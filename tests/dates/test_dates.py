# -*- coding: utf-8 -*-

from simpleplots.dates import (AutoDateLocator, YearLocator, MonthLocator,
                               WeekdayLocator, DayLocator, HourLocator,
                               MinuteLocator, SecondLocator, DateFormatter,
                               AutoDateFormatter)
import unittest
import numpy as np
import datetime

#-----------------------------------------------------------------------------

class TestDates(unittest.TestCase):

    def test_autodatelocator_seconds(self):
        loc = AutoDateLocator()

        dmin = np.datetime64('2022-01-01 01:01:01')
        dmax = np.datetime64('2022-01-01 01:01:59')
        delta = np.timedelta64(1, 's')
        times = np.arange(dmin, dmax, delta)

        to_test = loc.tick_values(np.min(times), np.max(times))
        expected = [
            datetime.datetime(2022, 1, 1, 1, 1, 10),
            datetime.datetime(2022, 1, 1, 1, 1, 20),
            datetime.datetime(2022, 1, 1, 1, 1, 30),
            datetime.datetime(2022, 1, 1, 1, 1, 40),
            datetime.datetime(2022, 1, 1, 1, 1, 50)
        ]
        self.assertListEqual(expected, to_test)

    def test_autodatelocator_minutes(self):
        loc = AutoDateLocator()

        dmin = np.datetime64('2022-01-01 01:01:01')
        dmax = np.datetime64('2022-01-01 01:12:34')
        delta = np.timedelta64(1, 'm')
        times = np.arange(dmin, dmax, delta)

        to_test = loc.tick_values(np.min(times), np.max(times))
        expected = [
            datetime.datetime(2022, 1, 1, 1, 5),
            datetime.datetime(2022, 1, 1, 1, 10)
        ]
        self.assertListEqual(expected, to_test)

    def test_autodatelocator_hours(self):
        loc = AutoDateLocator()

        dmin = np.datetime64('2022-01-01 01:01:01')
        dmax = np.datetime64('2022-01-01 13:12:34')
        delta = np.timedelta64(1, 'h')
        times = np.arange(dmin, dmax, delta)

        to_test = loc.tick_values(np.min(times), np.max(times))
        expected = [
            datetime.datetime(2022, 1, 1, 2, 0),
            datetime.datetime(2022, 1, 1, 4, 0),
            datetime.datetime(2022, 1, 1, 6, 0),
            datetime.datetime(2022, 1, 1, 8, 0),
            datetime.datetime(2022, 1, 1, 10, 0),
            datetime.datetime(2022, 1, 1, 12, 0)
        ]
        self.assertListEqual(expected, to_test)

    def test_autodatelocator_days(self):
        loc = AutoDateLocator()

        dmin = np.datetime64('2022-01-01 01:01:01')
        dmax = np.datetime64('2022-01-17 13:12:34')
        delta = np.timedelta64(1, 'D')
        times = np.arange(dmin, dmax, delta)

        to_test = loc.tick_values(np.min(times), np.max(times))
        expected = [
            datetime.datetime(2022, 1, 3, 0, 0),
            datetime.datetime(2022, 1, 5, 0, 0),
            datetime.datetime(2022, 1, 7, 0, 0),
            datetime.datetime(2022, 1, 9, 0, 0),
            datetime.datetime(2022, 1, 11, 0, 0),
            datetime.datetime(2022, 1, 13, 0, 0),
            datetime.datetime(2022, 1, 15, 0, 0),
            datetime.datetime(2022, 1, 17, 0, 0)
        ]
        self.assertListEqual(expected, to_test)

    def test_autodatelocator_months(self):
        loc = AutoDateLocator()

        dmin = np.datetime64('2022-01')
        dmax = np.datetime64('2022-06')
        delta = np.timedelta64(1, 'M')
        times = np.arange(dmin, dmax, delta).astype('datetime64[s]')

        to_test = loc.tick_values(np.min(times), np.max(times))
        expected = [
            datetime.datetime(2022, 1, 1, 0, 0),
            datetime.datetime(2022, 1, 15, 0, 0),
            datetime.datetime(2022, 2, 1, 0, 0),
            datetime.datetime(2022, 2, 15, 0, 0),
            datetime.datetime(2022, 3, 1, 0, 0),
            datetime.datetime(2022, 3, 15, 0, 0),
            datetime.datetime(2022, 4, 1, 0, 0),
            datetime.datetime(2022, 4, 15, 0, 0),
            datetime.datetime(2022, 5, 1, 0, 0)
        ]
        self.assertListEqual(expected, to_test)

    def test_autodatelocator_years(self):
        loc = AutoDateLocator()

        dmin = np.datetime64('2022-01')
        dmax = np.datetime64('2035-06')
        delta = np.timedelta64(1, 'Y')
        times = np.arange(dmin, dmax, delta).astype('datetime64[s]')

        to_test = loc.tick_values(np.min(times), np.max(times))
        expected = [
            datetime.datetime(2022, 1, 1, 0, 0),
            datetime.datetime(2024, 1, 1, 0, 0),
            datetime.datetime(2026, 1, 1, 0, 0),
            datetime.datetime(2028, 1, 1, 0, 0),
            datetime.datetime(2030, 1, 1, 0, 0),
            datetime.datetime(2032, 1, 1, 0, 0),
            datetime.datetime(2034, 1, 1, 0, 0),
            datetime.datetime(2036, 1, 1, 0, 0)
        ]
        self.assertListEqual(expected, to_test)

#-----------------------------------------------------------------------------
