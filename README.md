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

fig = uplot.figure('plotly5')
fig.plot(x, np.sin(x - 0*phi), name='#1')
fig.plot(x, np.sin(x - 1*phi), name='#2')
fig.plot(x, np.sin(x - 2*phi), name='#3')
fig.plot(x, np.sin(x - 3*phi), name='#4')
fig.xlabel('X')
fig.ylabel('Y')
fig.legend()
fig.show()
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
fig.xlabel('X')
fig.ylabel('Y')
fig.legend()
fig.show()
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

> See [gallery](gallery/gallery.md) for more examples.

## Install

Recent stable version (without any plotting library):
```bash
pip install "git+https://github.com/makarovdi/uplot.git@main"
```
To automatically install all optional dependencies (matplotlib, plotly, ...):
```bash
pip install "uplot[all] @ git+https://github.com/makarovdi/uplot.git@main"
```

If you need only `matplotlib` support:
```bash
pip install "uplot[matplotlib] @ git+https://github.com/makarovdi/uplot.git@main"
```
> Replace `[matplotlib]` with `[plotly5]` for plotly-only installation 


## Verified Versions

|                      |                                                Standalone |                                    JupyterLab<br>`4.0.6` |                           Jupyter<br/>Notebook<br/>`7.0` |                     IDE |
|:--------------------:|----------------------------------------------------------:|---------------------------------------------------------:|---------------------------------------------------------:|------------------------:|
| matplotlib<br/>`3.7` |      `gui` :green_circle:<br/>`save image` :green_circle: | `inline` :green_circle:<br/>`ipympl` :green_circle:<br/> | `inline` :green_circle:<br/>`ipympl` :green_circle:<br/> | `vscode` :green_circle: |
|  plotly<br/>`5.16`   | `chromium` :green_circle:<br/>`save image` :green_circle: |                                           :green_circle: |                                           :green_circle: | `vscode` :green_circle: |


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

## Extending

Adding a new engine is straightforward. Implement two interfaces `IPlotEngine` and `IFigure`:
```python
from uplot import IPlotEngine, IFigure

class MyEngine(IPlotEngine):
    ...
    def figure(self, ...) -> MyFigure: ...
    
class MyFigure(IFigure):
    def plot(self, ...): ...
    def scatter(self, ...): ...
    ...
```
Then use it in the regular way:
```python
import uplot

my_engine = MyEngine(...)


fig = uplot.figure(engine=my_engine)
fig.plot(...)
fig.show()
```

## Dependencies

- `Python` ≥ 3.10 
- `numpy` ≥ 1.21
- `pillow` ≥ 8.3

### Optional
- `matplotlib` ≥ 3.7
- `plotly` ≥  5.17


## License

This software is licensed under the `BSD-3-Clause` license.  
See the [LICENSE](LICENSE) file for details.

## TODO

Check the plan for new features [here](TODO.md).