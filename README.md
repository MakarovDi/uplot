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

The recent stable version (dependencies should be installed manually):
```bash
pip install git+https://github.com/makarovdi/uplot.git@main
```

With `matplotlib` package:
```bash
pip install git+https://github.com/makarovdi/uplot.git@main[matplotlib]
```

With `plotly` package:
```bash
pip install git+https://github.com/makarovdi/uplot.git@main[plotly5]
```

With all supported plotting libs:
```bash
pip install git+https://github.com/makarovdi/uplot.git@main[all]
```

## Tested

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


## License

This software is licensed under the `BSD-3-Clause` license.  
See the [LICENSE](LICENSE) file for details.

## TODO

- [ ] Gallery
- [ ] Changelog
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
- [ ] `DataFrame` support
- [ ] `Bokeh` engine