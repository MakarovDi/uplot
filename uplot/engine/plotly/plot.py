import numpy as np
from numpy.typing import ArrayLike

import uplot.color as ucolor
import uplot.utool as utool

from uplot.interface import LineStyle, MarkerStyle
from uplot.default import DEFAULT

from plotly.graph_objs import Figure


def plot_line_marker(figure      : Figure,
                     color       : str | list[str],
                     x           : ArrayLike,
                     y           : ArrayLike | None = None,
                     z           : ArrayLike | None = None,
                     name        : str | None = None,
                     line_style  : LineStyle | None = None,
                     line_width  : float = 2,
                     marker_style: MarkerStyle | None = None,
                     marker_size : int | None = None,
                     opacity     : float = 1.0,
                     **kwargs):
    """
    General plot: line, line+markers, markers(scatter).
    """
    x = np.atleast_1d(np.asarray(x))

    if y is None:
        y = x
        x = np.arange(len(y))
    else:
        y = np.asarray(y)

    y = np.atleast_1d(y)

    assert x.ndim == y.ndim == 1, 'the input must be 1d arrays'
    assert len(x) == len(y), 'the length of the input arrays must be the same'

    if z is not None:
        z = np.atleast_1d(np.asarray(z))
        assert z.ndim == 1, 'the input must be 1d arrays'
        assert len(x) == len(z), 'the length of the input arrays must be the same'

    if marker_size is None:
        # 1.33 - conversion gain between matplotlib and plotly marker size
        marker_size = DEFAULT.marker_size*1.33

    if name is None:
        name = ''
        show_legend = False
    else:
        show_legend = utool.kwargs_extract(kwargs, name='showlegend', default=True)

    if isinstance(color, str):
        color = ucolor.name_to_hex(color)
    else:
        # color specified for each point (x, y)
        color = [ ucolor.name_to_hex(c) for c in color]

    from uplot.engine.plotly.mapping import LINE_STYLE_MAPPING, MARKER_STYLE_MAPPING
    line_style = LINE_STYLE_MAPPING[line_style]
    marker_style = MARKER_STYLE_MAPPING[marker_style]

    line = utool.kwargs_extract(kwargs, name='line', default= {})
    marker = utool.kwargs_extract(kwargs, name='marker', default= {})

    mode = 'lines' if marker_style is None else 'lines+markers'
    if line_style == ' ': # no lines = scatter mode
        mode = 'markers'
        line['dash'] = None
    else:
        line.setdefault('color', color)
        line.setdefault('width', line_width)
        line['dash'] = line_style

    marker.setdefault('color', color)
    marker.setdefault('line_color', color)
    marker.setdefault('line_width', line_width)
    marker['symbol'] = marker_style
    marker['size'] = marker_size

    hoverlabel = utool.kwargs_extract(kwargs, name='hoverlabel', default= {})
    hoverlabel.setdefault('namelength', -1)

    if z is None:
        figure.add_scatter(x=x, y=y,
                           name=name,
                           mode=mode,
                           line=line,
                           marker=marker,
                           opacity=opacity,
                           showlegend=show_legend,
                           hoverlabel=hoverlabel,
                           **kwargs)
    else:
        figure.add_scatter3d(x=x, y=y, z=z,
                             name=name,
                             mode=mode,
                             line=line,
                             marker=marker,
                             opacity=opacity,
                             showlegend=show_legend,
                             hoverlabel=hoverlabel,
                             **kwargs)