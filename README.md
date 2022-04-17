![simpleplots](https://raw.githubusercontent.com/a-maliarov/simpleplots/main/ext/logo.png)
This library is created with the following idea in mind: "**If, for some reason, I need to create a lot of simple linear graphs and save their images, I don't want to worry about memory leaks. It must be easy to plot a simple 2D graph and save the figure, even if it's 100 of them!**"

---
Pure Python, lightweight, [Pillow](https://github.com/python-pillow/Pillow)-based plotting tool, **focused on efficiency and prevention of memory losses**. The project is, obviously, not trying to compete with [matplotlib](https://github.com/matplotlib/matplotlib) in data analysis, but aims to satisfy a specific purpose of **being able to create and save a large number of figures in the most efficient, yet accurate way**.

[![Status](https://img.shields.io/pypi/status/simpleplots)](https://pypi.org/project/simpleplots/)
[![Build Status](https://img.shields.io/circleci/build/github/a-maliarov/simpleplots)](https://app.circleci.com/pipelines/github/a-maliarov/simpleplots)
[![Coverage](https://img.shields.io/codecov/c/gh/a-maliarov/simpleplots?label=coverage)](https://codecov.io/gh/a-maliarov/simpleplots)
[![Version](https://img.shields.io/pypi/v/simpleplots?color=informational)](https://pypi.org/project/simpleplots/)
[![Python version](https://img.shields.io/badge/python-3.7%2B-informational)](https://pypi.org/project/simpleplots/)
[![Downloads](https://img.shields.io/pypi/dm/simpleplots?color=success)](https://pypi.org/project/simpleplots/)

## Installation
You can simply install the library from [PyPi](https://pypi.org/project/simpleplots/) using **pip**.
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

# Create a figure
fig = Figure()

# Plot data
fig.plot([2, 3, 4], [1, 4.3, 6], color='red', linewidth=7)
fig.plot([1, 3.5, 7], [2, 3, 5], color='blue', linewidth=10)

# Save the image (automatically closes the figure)
fig.save('graph.png')
```

Plotting dates:
```python
from simpleplots import Figure
from datetime import datetime
import numpy as np

# Create the data to be plotted
start, end = np.datetime64('2022-01-01'), np.datetime64('2022-01-20')
times = np.arange(start, end, np.timedelta64(1, 'D'))
values = np.random.randn(len(times))

# Create a figure
fig = Figure()

# Plot data
fig.plot(times, values, color='red', linewidth=7)

# Save the image (automatically closes the figure)
fig.save('graph.png')
```

Editing locators and formatters:
```python
from simpleplots import Figure
from simpleplots.dates import DateFormatter, HourLocator
from datetime import datetime
import numpy as np

# Create the data to be plotted
start, end = np.datetime64('2022-01-01 01'), np.datetime64('2022-01-01 23')
times = np.arange(start, end, np.timedelta64(1, 'h'))
values = np.random.randn(len(times))

# Create a figure
fig = Figure()

# Create and assign locator
locator = HourLocator()
fig.set_major_locator(locator, axis='x')

# Create and assign formatter
formatter = DateFormatter('%H:%M', rotation=45)
fig.set_major_formatter(formatter, axis='x')

# Plot data
fig.plot(times, values, color='red', linewidth=7)

# Save the image (automatically closes the figure)
fig.save('graph.png')
```

## Additional
+ *simpleplots* is a demand-driven library. In case you want to use *simpleplots*, but can't find a locator, formatter or functionality you need - leave a message by creating an issue.
