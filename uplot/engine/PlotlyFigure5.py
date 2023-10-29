from __future__ import annotations

import numpy as np
from typing import Literal
from numpy import ndarray
from numpy.typing import ArrayLike

import uplot.imtool as imtool

from uplot.interface import IFigure, LineStyle, MarkerStyle, AspectMode
from uplot.engine.PlotlyEngine5 import PlotlyEngine5
from uplot.color import default_colors_list, decode_color, default_colors
from uplot.routine import kwargs_extract


class PlotlyFigure5(IFigure):

    @property
    def engine(self) -> PlotlyEngine5:
        return self._engine

    @property
    def internal(self):
        return self._fig

    @property
    def is_3d(self) -> bool | None:
        return self._is_3d

    def __init__(self, engine: PlotlyEngine5):
        self._engine = engine
        self._color_index = 0

        self._fig: engine.figure_type = engine.go.Figure()
        self._is_3d = None


    def plot(self, x           : ArrayLike,
                   y           : ArrayLike | None = None,
                   z           : ArrayLike | None = None,
                   name        : str | None = None,
                   color       : str | list[str] | None = None,
                   line_style  : LineStyle | list[LineStyle] | None = None,
                   marker_style: MarkerStyle | list[MarkerStyle] | None = None,
                   marker_size : int | None = None,
                   opacity     : float = 1.0,
                   **kwargs):
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
            self._is_3d = True
        else:
            self._is_3d = False

        if marker_size is None:
            marker_size = self.engine.MARKER_SIZE

        if name is None:
            name = ''
            show_legend = False
        else:
            show_legend = True

        if color is None:
            color = self.current_color()
            self.scroll_color()
        elif not isinstance(color, str):
            # color specified for each point (x, y)
            color = [ decode_color(c) for c in color ]
        else:
            color = decode_color(color)

        line_style = LINE_STYLE_MAPPING[line_style]
        marker_style = MARKER_STYLE_MAPPING[marker_style]

        line = kwargs_extract(kwargs, name='line', default={})
        marker = kwargs_extract(kwargs, name='marker', default={})

        mode = 'lines' if marker_style is None else 'lines+markers'
        if line_style == ' ': # no lines = scatter mode
            mode = 'markers'
            line['dash'] = None
        else:
            line.setdefault('color', color)

        marker.setdefault('color', color)
        marker.setdefault('line_color', color)
        marker.setdefault('line_width', self.engine.LINE_WIDTH)
        marker['symbol'] = marker_style
        marker['size'] = marker_size

        hoverlabel = kwargs_extract(kwargs, name='hoverlabel', default={})
        hoverlabel.setdefault('namelength', -1)

        if not self._is_3d:
            self._fig.add_scatter(x=x, y=y,
                                  name=name,
                                  mode=mode,
                                  line=line,
                                  marker=marker,
                                  opacity=opacity,
                                  showlegend=show_legend,
                                  hoverlabel=hoverlabel)
        else:
            self._fig.add_scatter3d(x=x, y=y, z=z,
                                    name=name,
                                    mode=mode,
                                    line=line,
                                    marker=marker,
                                    opacity=opacity,
                                    showlegend=show_legend,
                                    hoverlabel=hoverlabel)

    def scatter(self, x           : ArrayLike,
                      y           : ArrayLike | None = None,
                      z           : ArrayLike | None = None,
                      name        : str | None = None,
                      color       : str | list[str] | None = None,
                      marker_style: MarkerStyle | list[MarkerStyle] | None = None,
                      marker_size : int | None = None,
                      opacity     : float = 1.0,
                      **kwargs):
        self.plot(x=x, y=y, z=z,
                  name=name,
                  line_style=' ',  # no line
                  color=color,
                  marker_style=marker_style,
                  marker_size=marker_size,
                  opacity=opacity,
                  **kwargs)

    def imshow(self, image: ArrayLike, **kwargs):
        image = np.asarray(image)
        value_range = imtool.estimate_range(image)

        self._is_3d = False

        self._fig.add_trace(self.engine.go.Image(
            z=image,
            zmax=kwargs_extract(kwargs, name='zmax', default=[value_range]*4),
            zmin=kwargs_extract(kwargs, name='zmin', default=[0]*4),
            **kwargs,
        ))

        # configure layout
        self._fig.update_layout(margin=self.engine.go.layout.Margin(b=30, t=30))
        self._fig.update_layout(hovermode='closest')
        self._fig.update_xaxes(visible=False)
        self._fig.update_yaxes(visible=False)

    def title(self, text: str):
        self._fig.update_layout(title=text)

    def legend(self, show: bool = True, **kwargs):
        self._fig.update_layout(legend=self.engine.go.layout.Legend(
            visible=show,
            bgcolor=kwargs_extract(kwargs, name='bgcolor', default='rgba(255,255,255,0.8)'),
            itemsizing=kwargs_extract(kwargs, name='itemsizing', default='constant'),
            **kwargs,
        ))

    def grid(self, show: bool = True):
        if self.is_3d:
            Scene = self.engine.go.layout.Scene
            XAxis = self.engine.go.layout.scene.XAxis
            YAxis = self.engine.go.layout.scene.YAxis
            ZAxis = self.engine.go.layout.scene.ZAxis
            self._fig.update_layout(scene=Scene(xaxis=XAxis(showgrid=show),
                                                yaxis=YAxis(showgrid=show),
                                                zaxis=ZAxis(showgrid=show))
            )
        else:
            self._fig.update_xaxes(showgrid=show)
            self._fig.update_yaxes(showgrid=show)

    def xlabel(self, text: str):
        self._fig.update_xaxes(title=text)

    def ylabel(self, text: str):
        self._fig.update_yaxes(title=text)

    def xlim(self, min_value: float | None = None,
                   max_value: float | None = None):
        update_axis_limit(figure=self._fig, axis='x',
                          range_min=min_value, range_max=max_value,
                          extra_space_percent=self.engine.RANGE_EXTRA_SPACE_PERCENT)

    def ylim(self, min_value: float | None = None,
                   max_value: float | None = None):
        update_axis_limit(figure=self._fig, axis='y',
                          range_min=min_value, range_max=max_value,
                          extra_space_percent=self.engine.RANGE_EXTRA_SPACE_PERCENT)

    def current_color(self) -> str:
        color_name = default_colors_list[self._color_index]
        return default_colors[color_name]

    def scroll_color(self, count: int=1):
        self._color_index += count
        self._color_index %= len(default_colors_list)

    def reset_color(self):
        self._color_index = 0

    def axis_aspect(self, mode: AspectMode):
        if mode == AspectMode.EQUAL:
            self._fig.update_yaxes(scaleanchor='x')
        else:
            self._fig.update_yaxes(scaleanchor=None)

    def as_image(self) -> ndarray:
        import io
        from PIL import Image

        fig_bytes = io.BytesIO(self._fig.to_image(format='png',
                                                  scale=self.engine.FILE_RESOLUTION_SCALE))
        image = Image.open(fig_bytes)
        image = np.asarray(image)
        image = image[..., :3] # RGBA -> RGB
        return image

    def save(self, fname: str):
        if '.html' in fname:
            self._fig.write_html(fname)
        else:
            self._fig.write_image(fname)

    def close(self):
        self._fig = None

    def show(self, block: bool = False):
        self.engine.pio.show(self._fig)


# TODO: update to 5.17
def update_axis_limit(figure, axis: Literal['x', 'y'],
                      range_min: float | None = None,
                      range_max: float | None = None,
                      extra_space_percent: int=2):
    # setting only min or only max is not implemented in plotly
    # https://github.com/plotly/plotly.js/issues/400
    # so manual estimation of min/max is required
    if (range_max is None or range_min is None) and not figure.data:
        raise RuntimeError('there is no any graph, use xlim/ylim after plotting or '
                           'specify both range_min and range_max')

    update_axis = {
        'x': figure.update_xaxes,
        'y': figure.update_yaxes,
    }[axis]

    get_axis_data = {
        'x': lambda trace: trace.x,
        'y': lambda trace: trace.y,
    }[axis]

    # min estimation
    if range_min is None:
        range_min = []
        for trace_data in figure.data:
            range_min.append(np.min(get_axis_data(trace_data)))
        range_min = np.min(range_min)

    # max estimation
    if range_max is None:
        range_max = []
        for trace_data in figure.data:
            range_max.append(np.max(get_axis_data(trace_data)))
        range_max = np.max(range_max)

    range_min *= 1 - np.sign(range_min) * extra_space_percent / 100
    range_max *= 1 + np.sign(range_max) * extra_space_percent / 100
    update_axis(range=[range_min, range_max])


LINE_STYLE_MAPPING: dict[LineStyle | None, str | None] = {
    '-' : 'solid',
    '--': 'dash',
    ':' : 'dot',
    '-.': 'dashdot',
    ''  : None,
    ' ' : ' ',
    None: None,
}

MARKER_STYLE_MAPPING: dict[MarkerStyle | None, str | None] = {
    '.': 'circle',
    ',': None,
    'o': 'circle-open',
    'v': 'triangle-down',
    '^': 'triangle-up',
    '<': 'triangle-left',
    '>': 'triangle-right',
    '1': 'y-down',
    '2': 'y-up',
    '3': 'y-left',
    '4': 'y-right',
    '8': 'octagon',
    's': 'square',
    'p': 'pentagon',
    '*': 'star',
    'h': 'hexagon',
    'H': 'hexagon2',
    '+': 'cross-thin',
    'x': 'x-thin',
    'X': 'x',
    'D': 'diamond',
    'd': 'diamond-tall',
    '|': 'line-ns',
    '_': 'line-ew',
    'P': 'cross',
    None: None,
}