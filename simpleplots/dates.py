# -*- coding: utf-8 -*-

"""
simpleplots.dates
~~~~~~~~~~~~~~~~~

All the locators located here are just a simplified version of what you can find
in matplotlib's (https://github.com/matplotlib/matplotlib) `dates` module.

If you want to understand the logic of calculation it is recommended to check
matplotlib's original code!

"""

__all__ = ('AutoDateLocator', 'YearLocator', 'MonthLocator', 'WeekdayLocator',
           'DayLocator', 'HourLocator', 'MinuteLocator', 'SecondLocator',
           'DateFormatter', 'AutoDateFormatter')

from .ticker import Locator, EdgeInteger, Formatter

from dateutil.relativedelta import relativedelta
import numpy as np
import dateutil.tz
import functools
import datetime

from dateutil.rrule import (rrule, MO, TU, WE, TH, FR, SA, SU, YEARLY,
                            MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY,
                            SECONDLY)

#-------------------------------------------------------------------------------

UTC = datetime.timezone.utc

MICROSECONDLY = SECONDLY + 1
HOURS_PER_DAY = 24.
MIN_PER_HOUR = 60.
SEC_PER_MIN = 60.
MONTHS_PER_YEAR = 12.

DAYS_PER_WEEK = 7.
DAYS_PER_MONTH = 30.
DAYS_PER_YEAR = 365.0

MINUTES_PER_DAY = MIN_PER_HOUR * HOURS_PER_DAY

SEC_PER_HOUR = SEC_PER_MIN * MIN_PER_HOUR
SEC_PER_DAY = SEC_PER_HOUR * HOURS_PER_DAY
SEC_PER_WEEK = SEC_PER_DAY * DAYS_PER_WEEK

MUSECONDS_PER_DAY = 1e6 * SEC_PER_DAY

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = (
    MO, TU, WE, TH, FR, SA, SU)
WEEKDAYS = (MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY)

#-------------------------------------------------------------------------------

def _get_tzinfo(tz=None):
    if tz is None:
        return UTC

    if isinstance(tz, str):
        tzinfo = dateutil.tz.gettz(tz)
        if tzinfo is None:
            raise ValueError(f"{tz} is not a valid timezone as parsed by"
                             " dateutil.tz.gettz.")
        return tzinfo

    if isinstance(tz, datetime.tzinfo):
        return tz

    raise TypeError("tz must be string or tzinfo subclass.")

class rrulewrapper:

    def __init__(self, freq, tzinfo=None, **kwargs):
        kwargs['freq'] = freq
        self._base_tzinfo = tzinfo

        self._update_rrule(**kwargs)

    def set(self, **kwargs):
        self._construct.update(kwargs)

        self._update_rrule(**self._construct)

    def _update_rrule(self, **kwargs):
        tzinfo = self._base_tzinfo

        if 'dtstart' in kwargs:
            dtstart = kwargs['dtstart']
            if dtstart.tzinfo is not None:
                if tzinfo is None:
                    tzinfo = dtstart.tzinfo
                else:
                    dtstart = dtstart.astimezone(tzinfo)

                kwargs['dtstart'] = dtstart.replace(tzinfo=None)

        if 'until' in kwargs:
            until = kwargs['until']
            if until.tzinfo is not None:
                if tzinfo is not None:
                    until = until.astimezone(tzinfo)
                else:
                    raise ValueError('until cannot be aware if dtstart '
                                     'is naive and tzinfo is None')

                kwargs['until'] = until.replace(tzinfo=None)

        self._construct = kwargs.copy()
        self._tzinfo = tzinfo
        self._rrule = rrule(**self._construct)

    def _attach_tzinfo(self, dt, tzinfo):
        if hasattr(tzinfo, 'localize'):
            return tzinfo.localize(dt, is_dst=True)

        return dt.replace(tzinfo=tzinfo)

    def _aware_return_wrapper(self, f, returns_list=False):
        if self._tzinfo is None:
            return f

        def normalize_arg(arg):
            if isinstance(arg, datetime.datetime) and arg.tzinfo is not None:
                if arg.tzinfo is not self._tzinfo:
                    arg = arg.astimezone(self._tzinfo)

                return arg.replace(tzinfo=None)

            return arg

        def normalize_args(args, kwargs):
            args = tuple(normalize_arg(arg) for arg in args)
            kwargs = {kw: normalize_arg(arg) for kw, arg in kwargs.items()}

            return args, kwargs

        if not returns_list:
            def inner_func(*args, **kwargs):
                args, kwargs = normalize_args(args, kwargs)
                dt = f(*args, **kwargs)
                return self._attach_tzinfo(dt, self._tzinfo)
        else:
            def inner_func(*args, **kwargs):
                args, kwargs = normalize_args(args, kwargs)
                dts = f(*args, **kwargs)
                return [self._attach_tzinfo(dt, self._tzinfo) for dt in dts]

        return functools.wraps(f)(inner_func)

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        f = getattr(self._rrule, name)

        if name in {'after', 'before'}:
            return self._aware_return_wrapper(f)
        elif name in {'xafter', 'xbefore', 'between'}:
            return self._aware_return_wrapper(f, returns_list=True)
        else:
            return f

    def __setstate__(self, state):
        self.__dict__.update(state)

#-------------------------------------------------------------------------------

class DateFormatter(Formatter):

    def __init__(self, fmt, tz=None, rotation=None):
        self.fmt = fmt
        self.tz = _get_tzinfo(tz)
        self.rotation = rotation

    def __call__(self, value):
        return value.astype(datetime.datetime).strftime(self.fmt)

class AutoDateFormatter(Formatter):

    def __init__(self, defaultfmt='%Y-%m-%d', rotation=45):
        self.defaultfmt = defaultfmt
        self.rotation = rotation

    def __call__(self, value):
        formatter = DateFormatter(self.defaultfmt, rotation=self.rotation)
        return formatter(value)

#-------------------------------------------------------------------------------

class DateLocator(Locator):
    hms0d = {'byhour': 0, 'byminute': 0, 'bysecond': 0}

    def __init__(self, tz=None):
        self.tz = _get_tzinfo(tz)

#-------------------------------------------------------------------------------

class RRuleLocator(DateLocator):

    def __init__(self, o, tz=None):
        super().__init__(tz)
        self.rule = o

    def tick_values(self, vmin, vmax):
        vmin = vmin.astype(datetime.datetime)
        vmax = vmax.astype(datetime.datetime)
        start, stop = self._create_rrule(vmin, vmax)

        dates = self.rule.between(start, stop, True)

        if len(dates) == 0:
            return [vmin, vmax]
        return dates

    def _create_rrule(self, vmin, vmax):
        delta = relativedelta(vmax, vmin)

        try:
            start = vmin - delta
        except (ValueError, OverflowError):
            start = datetime.datetime(1, 1, 1, 0, 0, 0,
                                      tzinfo=datetime.timezone.utc)

        try:
            stop = vmax + delta
        except (ValueError, OverflowError):
            stop = datetime.datetime(9999, 12, 31, 23, 59, 59,
                                     tzinfo=datetime.timezone.utc)

        self.rule.set(dtstart=start, until=stop)

        return vmin, vmax

#-------------------------------------------------------------------------------

class YearLocator(RRuleLocator):

    def __init__(self, base=1, month=1, day=1, tz=None):
        rule = rrulewrapper(YEARLY, interval=base, bymonth=month,
                            bymonthday=day, **self.hms0d)
        super().__init__(rule, tz=tz)
        self.base = EdgeInteger(base, 0)

    def _create_rrule(self, vmin, vmax):
        ymin = max(self.base.le(vmin.year) * self.base.step, 1)
        ymax = min(self.base.ge(vmax.year) * self.base.step, 9999)

        c = self.rule._construct
        replace = {'year': ymin,
                   'month': c.get('bymonth', 1),
                   'day': c.get('bymonthday', 1),
                   'hour': 0, 'minute': 0, 'second': 0}

        start = vmin.replace(**replace)
        stop = start.replace(year=ymax)
        self.rule.set(dtstart=start, until=stop)

        return start, stop

class MonthLocator(RRuleLocator):

    def __init__(self, bymonth=None, bymonthday=1, interval=1, tz=None):
        if bymonth is None:
            bymonth = range(1, 13)
        elif isinstance(bymonth, np.ndarray):
            bymonth = [x.item() for x in bymonth.astype(int)]

        rule = rrulewrapper(MONTHLY, bymonth=bymonth, bymonthday=bymonthday,
                            interval=interval, **self.hms0d)
        super().__init__(rule, tz=tz)

class WeekdayLocator(RRuleLocator):

    def __init__(self, byweekday=1, interval=1, tz=None):
        if isinstance(byweekday, np.ndarray):
            [x.item() for x in byweekday.astype(int)]

        rule = rrulewrapper(DAILY, byweekday=byweekday,
                            interval=interval, **self.hms0d)
        super().__init__(rule, tz=tz)

class DayLocator(RRuleLocator):

    def __init__(self, bymonthday=None, interval=1, tz=None):
        if interval != int(interval) or interval < 1:
            raise ValueError("interval must be an integer greater than 0")
        if bymonthday is None:
            bymonthday = range(1, 32)
        elif isinstance(bymonthday, np.ndarray):
            bymonthday = [x.item() for x in bymonthday.astype(int)]

        rule = rrulewrapper(DAILY, bymonthday=bymonthday,
                            interval=interval, **self.hms0d)
        super().__init__(rule, tz=tz)

class HourLocator(RRuleLocator):

    def __init__(self, byhour=None, interval=1, tz=None):
        if byhour is None:
            byhour = range(24)

        rule = rrulewrapper(HOURLY, byhour=byhour, interval=interval,
                            byminute=0, bysecond=0)
        super().__init__(rule, tz=tz)

class MinuteLocator(RRuleLocator):

    def __init__(self, byminute=None, interval=1, tz=None):
        if byminute is None:
            byminute = range(60)

        rule = rrulewrapper(MINUTELY, byminute=byminute, interval=interval,
                            bysecond=0)
        super().__init__(rule, tz=tz)

class SecondLocator(RRuleLocator):

    def __init__(self, bysecond=None, interval=1, tz=None):
        if bysecond is None:
            bysecond = range(60)

        rule = rrulewrapper(SECONDLY, bysecond=bysecond, interval=interval)
        super().__init__(rule, tz=tz)

#-------------------------------------------------------------------------------

class AutoDateLocator(DateLocator):

    def __init__(self, tz=None, minticks=6, maxticks=10,
                 interval_multiples=True):

        super().__init__(tz=tz)
        self._freq = YEARLY
        self._freqs = [YEARLY, MONTHLY, DAILY, HOURLY, MINUTELY,
                       SECONDLY, MICROSECONDLY]

        self.minticks = minticks

        self.maxticks = {YEARLY: 11, MONTHLY: 12, DAILY: 11, HOURLY: 12,
                         MINUTELY: 11, SECONDLY: 11, MICROSECONDLY: 8}

        if maxticks is not None:
            try:
                self.maxticks.update(maxticks)
            except TypeError:
                self.maxticks = dict.fromkeys(self._freqs, maxticks)
        self.interval_multiples = interval_multiples

        self.intervald = {
            YEARLY:   [1, 2, 4, 5, 10, 20, 40, 50, 100, 200, 400, 500,
                       1000, 2000, 4000, 5000, 10000],
            MONTHLY:  [1, 2, 3, 4, 6],
            DAILY:    [1, 2, 3, 7, 14, 21],
            HOURLY:   [1, 2, 3, 4, 6, 12],
            MINUTELY: [1, 5, 10, 15, 30],
            SECONDLY: [1, 5, 10, 15, 30]
        }

        if interval_multiples:
            self.intervald[DAILY] = [1, 2, 4, 7, 14]

        self._byranges = [None, range(1, 13), range(1, 32),
                          range(0, 24), range(0, 60), range(0, 60), None]

    def tick_values(self, vmin, vmax):
        if vmin == vmax:
            return [vmin]
        return self.get_locator(vmin, vmax).tick_values(vmin, vmax)

    def get_locator(self, dmin, dmax):
        dmin = dmin.astype(datetime.datetime)
        dmax = dmax.astype(datetime.datetime)
        delta = relativedelta(dmax, dmin)
        tdelta = dmax - dmin

        if dmin > dmax:
            delta = -delta
            tdelta = -tdelta

        numYears = float(delta.years)
        numMonths = numYears * MONTHS_PER_YEAR + delta.months
        numDays = tdelta.days
        numHours = numDays * HOURS_PER_DAY + delta.hours
        numMinutes = numHours * MIN_PER_HOUR + delta.minutes
        numSeconds = np.floor(tdelta.total_seconds())
        numMicroseconds = np.floor(tdelta.total_seconds() * 1e6)

        nums = [numYears, numMonths, numDays, numHours, numMinutes,
                numSeconds, numMicroseconds]

        use_rrule_locator = [True] * 6 + [False]

        byranges = [None, 1, 1, 0, 0, 0, None]

        for i, (freq, num) in enumerate(zip(self._freqs, nums)):
            if num < self.minticks:
                byranges[i] = None
                continue

            for interval in self.intervald[freq]:
                if num <= interval * (self.maxticks[freq] - 1):
                    break
            else:
                if not (self.interval_multiples and freq == DAILY):
                    print(f"AutoDateLocator was unable to pick an appropriate "
                          f"interval for this date range. It may be necessary "
                          f"to add an interval value to the AutoDateLocator's "
                          f"intervald dictionary. Defaulting to {interval}.")

            self._freq = freq

            if self._byranges[i] and self.interval_multiples:
                byranges[i] = self._byranges[i][::interval]
                if i in (DAILY, WEEKLY):
                    if interval == 14:
                        byranges[i] = [1, 15]
                    elif interval == 7:
                        byranges[i] = [1, 8, 15, 22]

                interval = 1
            else:
                byranges[i] = self._byranges[i]
            break
        else:
            interval = 1

        if (freq == YEARLY) and self.interval_multiples:
            locator = YearLocator(interval, tz=self.tz)
        elif use_rrule_locator[i]:
            _, bymonth, bymonthday, byhour, byminute, bysecond, _ = byranges
            rrule = rrulewrapper(self._freq, interval=interval,
                                 dtstart=dmin, until=dmax,
                                 bymonth=bymonth, bymonthday=bymonthday,
                                 byhour=byhour, byminute=byminute,
                                 bysecond=bysecond)

            locator = RRuleLocator(rrule, tz=self.tz)

        return locator

#-------------------------------------------------------------------------------
