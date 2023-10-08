# uplot

[![python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)](https://docs.python.org/3/whatsnew/3.10.html)
[![license](https://img.shields.io/badge/License-BSD%203--Clause-green)](https://choosealicense.com/licenses/mit/)
[![jupyter](https://img.shields.io/badge/Jupyter-Lab-F37626.svg?style=flat&logo=Jupyter)](https://jupyterlab.readthedocs.io/en/stable)

Unified API and style for Python plotting libraries.

## Usage

```python
import uplot

f = uplot.figure(engine='matplotlib')
f.plot([1, 2, 3], [1, 2, 3], name='Line 45')
f.legend(show=True)
f.title('Test')
f.xlabel('X')
f.ylabel('Y')
f.show(block=True)
```

## Install

The recent stable version (without any plotting library):
```bash
pip install git+https://github.com/makarovdi/uplot.git@main
```
to automatically install all dependencies run
```bash
pip install git+https://github.com/makarovdi/uplot.git@main[all]
```

If you need only `matplotlib` support:
```bash
pip install git+https://github.com/makarovdi/uplot.git@main[matplotlib]
```
> Replace `[matplotlib]` with `[plotly5]` for plotly only installation 


## Verified Versions

|                      |                      Standalone |          JupyterLab<br>`4.0.6` | Jupyter<br/>Notebook<br/>`7.0` |         IDE |
|:--------------------:|--------------------------------:|-------------------------------:|-------------------------------:|------------:|
| matplotlib<br/>`3.7` |      `gui` ✔<br/>`save image` ✔ | `inline` ✔<br/>`ipympl` ✔<br/> | `inline` ✔<br/>`ipympl` ✔<br/> |  `vscode` ✔ |
|  plotly<br/>`5.17`   | `chromium` ✔<br/>`save image` ✔ |                              ✔ |                              ✔ |  `vscode` ✔ |


## Dependencies

- `Python` ≥ 3.10 
- `numpy` ≥ 1.21
- `pillow` ≥ 8.3

### Optional
- `matplotlib` ≥ 3.7
- `plotly` ≥  5.17

## Plotting Libs - Pros & Cons

### matplotlib

:green_circle: Highly configurable.  
:green_circle: Support multiple GUI-backends.  
:green_circle: Good documentation and a lot of ready-to-use recipes (e.g. on StackOverflow).  
:yellow_circle: Common API (MATLAB legacy). 
  
 
:red_circle: Limited interactivity (especially for Jupyter).  
:red_circle: Inconsistent API, behaviour and a function parameter names (e.g. plt.xlim and axis.set_xlim).  
&emsp;`->` It's easy to spend an entire day setting up something simple (like a legend location).   
:red_circle: Slow, cumbersome and inconsistent API for 3D graphs.   


### plotly

:green_circle: Very good interactively.  
:green_circle: Native compatibility with Jupyter.  
:green_circle: Possibility to save interactive plot (html-file).  
:green_circle: Fast and interactive 3D plot.  
:yellow_circle: Good API design (especially compared to matplotlib). 

:red_circle: Not well documented (a lot of parameters, small amount of examples).  
:red_circle: High memory consumption (limited number of plots in Jupyter).  
:red_circle: Some expected API functions are missing (e.g. imshow).  
:red_circle: 3D and 2D axis parameters are not unified (layout.xaxis doesn't work for 3D).   

## Extending

Adding a new engine is straightforward. You should implement two interfaces `IPlotEngine` and `IFigure`:
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
Then it can be used in the regular way:
```python
import uplot

my_engine = MyEngine(...)


fig = uplot.figure(engine=my_engine)
fig.plot(...)
fig.show()
```


## License

This software is licensed under the `BSD-3-Clause` license.  
See the [LICENSE](LICENSE) file for details.

## TODO

- [ ] Gallery
- [x] Changelog
- [x] **API**: aspect ratio param: `uplot.figure(..., aspect_ratio: float)`
- [ ] **API**: `fig.plot3d(...)` and `fig.scatter3d(...)`
- [ ] **API**: `fig.surface3d(...)`
- [ ] **API**: `opacity: float` -> `opacity: float | list[float]`
- [ ] **API**: plugin system for plotting of a custom object: `fig.visualize(obj)`
- [ ] **API**: `fig.bar(...)` 
- [ ] **API**: `fig.click_event(...)`
- [ ] **API**: `fig.legend_group(...)`
- [ ] **API**: `fig.hover_text(...)`
- [ ] **API**: `kwargs` to directly access underlying engine 
- [ ] **API**: `fig.legend`: param for the legend location
- [ ] `DataFrame` support
- [ ] `Bokeh` engine