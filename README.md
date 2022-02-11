![simpleplots](https://raw.githubusercontent.com/a-maliarov/simpleplots/main/ext/logo.png)
This library is created with the following idea in mind: "**If, for some reason, I need to create a lot of simple linear graphs and save their images, I don't want to worry about memory leaks. It must be easy to plot a simple 2D graph and save the figure, even if it's 100 of them!**"

---
Pure Python, lightweight, [Pillow](https://github.com/python-pillow/Pillow)-based plotting tool, focused on efficiency and prevention of memory losses.

[![Status](https://img.shields.io/pypi/status/simpleplots)](https://pypi.org/project/simpleplots/)
[![Version](https://img.shields.io/pypi/v/simpleplots?color=informational)](https://pypi.org/project/simpleplots/)
[![Python version](https://img.shields.io/badge/python-3.7%2B-informational)](https://pypi.org/project/simpleplots/)
[![Downloads](https://img.shields.io/pypi/dm/simpleplots?color=success)](https://pypi.org/project/simpleplots/)

## Recent News
+ *February 9, 2022*: added float numbers support
+ *February 9, 2022*: tested and approved compatibility with Pillow 9.0.1
+ *February 8, 2022*: added int numbers support

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
