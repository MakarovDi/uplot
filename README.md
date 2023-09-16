# uplot

[![python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)](https://docs.python.org/3/whatsnew/3.10.html)
[![python](https://img.shields.io/badge/License-BSD%203--Clause-green)](https://choosealicense.com/licenses/mit/)
[![jupyter](https://img.shields.io/badge/Jupyter-Lab-F37626.svg?style=flat&logo=Jupyter)](https://jupyterlab.readthedocs.io/en/stable)

Unified API and style for Python plotting libraries.

## Usage

```python
import uplot

f = uplot.figure(engine='matplot')
f.plot([1, 2, 3], [1, 2, 3], name='Line 45')
f.legend(show=True)
f.title('Test')
f.xlabel('X')
f.ylabel('Y')
f.show(block=True)
```

## Install

```bash
pip install git+https://github.com/makarovdi/uplot.git
```

## Tested

|                     | GUI                             | JupyterLab<br>`4.0.6`                      | Jupyter<br>Notebook<br>`7.0`               | IPython<br>`x.x` | VSCode<br> |
|:-------------------:|:--------------------------------|:-------------------------------------------|:-------------------------------------------|:-----------------|:-----------|
| matplotlib<br>`3.7` | `windows` &#10004;<br>          | `inline` &#10004;<br>`ipympl` &#10004;<br>  | `inline` &#10004;<br>`ipympl` &#10004;<br> | &quest;          | &quest;          |


## Dependencies

- Python >= `3.10` 
- numpy

### Optional
- matplotlib >= `3.7`
- plotly >= `5.0`


## License

This software is licensed under the BSD-3-Clause license.  
See the [LICENSE](LICENSE) file for details.

## TODO

- [ ] Plugin system for plotting of a custom object.
- [ ] API: `fig.bar(...)` 
- [ ] `DataFrame` support
- [ ] `Bokeh` engine