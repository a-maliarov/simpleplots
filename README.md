![simpleplots](https://raw.githubusercontent.com/a-maliarov/simpleplots/main/ext/logo.png)
This library is created with the following idea in mind: "**If, for some reason, I need to create a lot of simple linear graphs and save their images, I don't want to worry about memory leaks. It must be easy to plot a simple 2D graph and save the figure, even if it's 100 of them!**"

---
Pure Python, lightweight, [Pillow](https://github.com/python-pillow/Pillow)-based plotting tool, focused on efficiency and prevention of memory losses. The project is, obviously, not trying to compete with [matplotlib](https://github.com/matplotlib/matplotlib) in data analysis, but aims to satisfy a specific purpose of being able to create and save a large number of figures in the most efficient, yet accurate way.

[![Status](https://img.shields.io/pypi/status/simpleplots)](https://pypi.org/project/simpleplots/)
[![Build Status](https://app.travis-ci.com/a-maliarov/simpleplots.svg?branch=main)](https://app.travis-ci.com/github/a-maliarov/simpleplots)
[![Code Coverage](https://img.shields.io/codecov/c/gh/a-maliarov/simpleplots?label=code%20coverage)](https://codecov.io/gh/a-maliarov/simpleplots)
[![Version](https://img.shields.io/pypi/v/simpleplots?color=informational)](https://pypi.org/project/simpleplots/)
[![Python version](https://img.shields.io/badge/python-3.7%2B-informational)](https://pypi.org/project/simpleplots/)
[![Downloads](https://img.shields.io/pypi/dm/simpleplots?color=success)](https://pypi.org/project/simpleplots/)

## Installation
You can simply install the library from [PyPi](https://pypi.org/project/amazoncaptcha/) using **pip**.
```bash
pip install simpleplots
```

## Quick Snippet
An example of the basic usage. Method `.save` automatically closes the figure by default.
```python
from simpleplots import Figure

fig = Figure()
fig.plot([2, 3, 4], [4, 2, 3], color='red')
fig.save('graph.png')
```

## Performance
*The data has been collected using [memory_profiler](https://github.com/pythonprofilers/memory_profiler) module. You can find more tests [here](https://github.com/a-maliarov/simpleplots/tree/main/comparizon)*.
![simpleplots](https://github.com/a-maliarov/simpleplots/blob/main/comparizon/200_points_1_axes/200_points_results.png?raw=true)

## Usage Samples
The library also supports plotting multiple axes within one figure.
```python
from simpleplots import Figure

fig = Figure()
fig.plot([2, 3, 4], [1, 4.3, 6], color='red', linewidth=7)
fig.plot([1, 3.5, 7], [2, 3, 5], color='blue', linewidth=7)
fig.save('graph.png')
```

## Additional
+ simpleplots is currently in developement.
