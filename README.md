# uplot

[![python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)](https://docs.python.org/3/whatsnew/3.10.html)
[![license](https://img.shields.io/badge/License-BSD%203--Clause-green)](https://choosealicense.com/licenses/mit/)
[![jupyter](https://img.shields.io/badge/Jupyter-Lab-F37626.svg?style=flat&logo=Jupyter)](https://jupyterlab.readthedocs.io/en/stable)

Unified API and style for Python plotting libraries.

## Usage

<table style="border-collapse: collapse; border-style: hidden;">

<tr>
<td> <b>plotly 5</b> </td> <td> <b>matplotlib</b> </td>
</tr>

<tr>
<td>

```python
import numpy as np
import uplot

x = np.linspace(0, np.pi*4, num=100)
phi = np.pi/4

fig = uplot.figure('plotly')
fig.plot(x, np.sin(x - 0*phi), name='#1')
fig.plot(x, np.sin(x - 1*phi), name='#2')
fig.plot(x, np.sin(x - 2*phi), name='#3')
fig.plot(x, np.sin(x - 3*phi), name='#4')
fig.xlabel('X').ylabel('Y')
fig.legend().show()
```

</td>
<td>

```python
import numpy as np
import uplot

x = np.linspace(0, np.pi*4, num=100)
phi = np.pi/4

fig = uplot.figure('matplotlib')
fig.plot(x, np.sin(x - 0*phi), name='#1')
fig.plot(x, np.sin(x - 1*phi), name='#2')
fig.plot(x, np.sin(x - 2*phi), name='#3')
fig.plot(x, np.sin(x - 3*phi), name='#4')
fig.xlabel('X').ylabel('Y')
fig.legend().show()
```

</td>
</tr>

<tr>
<td>

<img src='gallery/asset/plotly5-example.png' width='380'>

</td>

<td>

<img src='gallery/asset/mpl-example.png' width='380'>

</td>

</tr>
</table>

> :bulb: See [gallery](gallery/gallery.md) for more examples.

## Install

Recent stable version (without any plotting library):
```bash
pip install "uplot @ git+https://github.com/makarovdi/uplot.git@main"
```
To automatically install all optional dependencies (matplotlib, plotly, ...):
```bash
pip install "uplot[all] @ git+https://github.com/makarovdi/uplot.git@main"
```

If you need only `matplotlib` support:
```bash
pip install "uplot[matplotlib] @ git+https://github.com/makarovdi/uplot.git@main"
```
> :bulb: Replace `[matplotlib]` with `[plotly5]` for plotly-only installation 


## Plotting Libs - Pros & Cons

### [Matplotlib](https://matplotlib.org/)

:green_circle: Highly configurable.  
:green_circle: Good documentation and a lot of ready-to-use recipes (e.g. on StackOverflow).  
:yellow_circle: Common API (MATLAB legacy). 
  
 
:red_circle: Limited interactivity (especially for Jupyter).  
:red_circle: API, behavior and parameter names are inconsistent (e.g. plt.xlim and axis.set_xlim).  
:red_circle: Slow and limited 3D rendering.   


### [Plotly](https://plotly.com/python/)

:green_circle: Very good interactivity.  
:green_circle: Native compatibility with Jupyter.  
:green_circle: Possibility to save interactive plot (html-file).  
:green_circle: Fast and interactive 3D plot.  

:red_circle: Not well documented (a lot of parameters, small amount of examples).  
:red_circle: High memory consumption (limited number of plots in Jupyter).  
:red_circle: Some expected API functions are missing (e.g. imshow).  
:red_circle: 3D and 2D axis parameters are not unified (e.g. layout.xaxis doesn't work for 3D).   

## Functions

| Function                                                      | Description                                                                                                                                                   |
|:--------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `plot(x, y, z)` <br/> `plot(obj)`                             | Plot 2D or 3D line. <br/>Line plot for custom class (supported by a plugin).                                                                                  |
| `scatter(x, y, z)` <br/> `scatter(obj)`                       | Scatter plot for 2D or 3D data points. <br/> Scatter plot for custom class (supported by a plugin).                                                           |
| `hline(y)` <br/> `vline(x)`                                   | Plot horizontal or vertical line. `2D plot only`                                                                                                              |
| `surface3d(x, y, z)`                                          | Plot a surface in 3D space where the color scale corresponds to the z-values.                                                                                 |
| `imshow(image)`                                               | Display an image.                                                                                                                                             |
| `title(text)`                                                 | Set the title of the figure.                                                                                                                                  |
| `legend(show)`                                                | Show or hide the legend on the figure.                                                                                                                        |
| `grid(show)`                                                    | Show or hide the grid on the figure.                                                                                                                          |
| `xlabel(text)` <br/> `ylabel(text)` <br/> `zlabel(text)`            | Set the label for the x, y, z-axis.                                                                                                                           |
| `xlim(min, max)` <br/> `ylim(min, max)` <br/> `zlim(min, max)`      | Set limits for the x, y, z-axis.                                                                                                                              |
| `current_color()` <br/> `scroll_color(count)` <br/> `reset_color()` | Get the color which will be used for the next plot. <br/> Scroll a list of predefined colors for plots. <br/> Set the current color to the start of the list. |
| `axis_aspect(mode)`                                             | Set the aspect ratio of the axis.                                                                                                                                                              |
| `as_image()`                                                    | Get the figure as a numpy array.                                                                                                                                                              |
| `save(filename)`                                                | Save the figure to a file.                                                                                                                                                              |
| `close()`                                                       | Close the figure. Free allocated resources.                                                                                                                                                              |
| `show(block)`                                                   | Display the figure.                                                                                                                                                              |


## Extending


### Plugin

The plugin system allows extending `uplot` for visualizing custom objects.   
For example, the `DataFrame` plugin enables this code:
```python
import uplot
import pandas as pd

car_crashes = pd.read_csv(
    'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/car_crashes.csv'
)

fig = uplot.figure()
fig.plot(car_crashes[['total', 'speeding', 'alcohol', 'no_previous']])
fig.show()
```
<img src='gallery/asset/plugin.png' width='480'>

To implement the plugin, you can follow this structure:
```python
import numpy as np
import pandas as pd

import uplot.plugin as plugin


class DataFramePlugin(plugin.IPlotPlugin):

    def extract_data(self, obj: pd.DataFrame) -> list[plugin.PlotData]:
        data = []
        for name in obj.columns:
            if not np.issubdtype(obj.dtypes[name], np.number): continue
            y = obj[name].values
            x = np.arange(len(y))
            data.append(plugin.PlotData(x=x, y=y, name=name.replace('_', ' ').title()))
        return data

plugin.register(pd.DataFrame, handler=DataFramePlugin())
```

> :bulb: Check `test/plugin.py` for a more advanced plugin example. 

### Engine

Adding a new plotting library is straightforward. Implement two interfaces `IPlotEngine` and `IFigure`:
```python
import uplot
from uplot import IPlotEngine, IFigure

class MyEngine(IPlotEngine):
    ...
    def figure(self, ...) -> MyFigure: ...
    
class MyFigure(IFigure):
    def plot(self, ...): ...
    def scatter(self, ...): ...
    ...

# register the engine
uplot.engine.register(MyEngine(), name='test') 
```
Then use it in the regular way:
```python
import uplot

fig = uplot.figure(engine='test')
fig.plot(...)
fig.show()
```

## Dependencies

- `Python` ≥ 3.10 
- `numpy` ≥ 1.21 `v2.0 supported`
- `pillow` ≥ 10.2

### Optional
- `matplotlib` ≥ 3.7
- `plotly` ≥  5.17


## License

This software is licensed under the `BSD-3-Clause` license.  
See the [LICENSE](LICENSE) file for details.

## TODO

Check the plan for new features [here](TODO.md).