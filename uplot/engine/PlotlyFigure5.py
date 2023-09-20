from __future__ import annotations

import numpy as np
from typing import Literal
from numpy import ndarray
from numpy.typing import ArrayLike

import uplot.imtool as imtool

from uplot.interface import IFigure, LineStyle, MarkerStyle
from uplot.engine.PlotlyEngine5 import PlotlyEngine5
from uplot.colors import default_colors_list, decode_color, default_colors
from uplot.routine import unpack_param


class PlotlyFigure5(IFigure):
    DEFAULT_MARKER_SIZE = 8
    DEFAULT_LINE_WIDTH = 2
    RANGE_EXTRA_SPACE_PERCENT = 2 # adding extra space to min/max ranges

    @property
    def engine(self) -> PlotlyEngine5:
        return self._engine

    @property
    def internal(self):
        return self._fig


    def __init__(self, engine: PlotlyEngine5):
        self._engine = engine
        self._color_index = 0

        self._fig: engine.figure_type = engine.go.Figure()


    def plot(self, x          : ArrayLike,
                   y          : ArrayLike | None = None,
                   name       : str | list[str] | None = None,
                   color      : str | list[str] | None = None,
                   line       : LineStyle | list[LineStyle] | None = None,
                   marker     : MarkerStyle | list[MarkerStyle] | None = None,
                   marker_size: int | None = None,
                   opacity    : float = 1.0):
        x = np.atleast_1d(np.asarray(x))

        if y is not None:
            y = np.asarray(y)
        else:
            y = x
            x = np.arange(len(y))

        y = y.reshape([len(x), -1])

        if marker_size is None:
            marker_size = self.DEFAULT_MARKER_SIZE

        for i, y_i in enumerate(y.T):
            name_i = unpack_param(name, i)
            if name_i is None:
                name_i = ''
                show_legend = False
            else:
                show_legend = True

            color_i = decode_color(unpack_param(color, i))
            if color_i is None:
                color_i = self.current_color()
                self.scroll_color()

            line_i = LINE_STYLE_MAPPING[unpack_param(line, i)]
            marker_i = MARKER_STYLE_MAPPING[unpack_param(marker, i)]

            mode = 'lines' if marker_i is None else 'lines+markers'
            if line_i == ' ':
                mode = 'markers'
                line_i = None

            self._fig.add_scatter(x=x, y=y_i,
                                  name=name_i,
                                  mode=mode,
                                  line_color=color_i,
                                  line=self.engine.go.scatter.Line(dash=line_i),
                                  marker=self.engine.go.scatter.Marker(symbol=marker_i,
                                                                       line_color=color_i,
                                                                       line_width=self.DEFAULT_LINE_WIDTH,
                                                                       size=marker_size),
                                  opacity=opacity,
                                  showlegend=show_legend)

    def scatter(self, x          : ArrayLike,
                      y          : ArrayLike | None = None,
                      name       : str | list[str] | None = None,
                      color      : str | list[str] | None = None,
                      marker     : MarkerStyle | list[MarkerStyle] | None = None,
                      marker_size: int | None = None,
                      opacity    : float = 1.0):
        self.plot(x=x, y=y,
                  name=name,
                  line=' ', # no line
                  color=color,
                  marker=marker,
                  marker_size=marker_size,
                  opacity=opacity)

    def imshow(self, image: ArrayLike):
        image = np.asarray(image)

        # configure layout
        self._fig.update_layout(margin=self.engine.go.layout.Margin(b=30, t=30))
        self._fig.update_layout(hovermode='closest')
        self._fig.update_xaxes(visible=False)
        self._fig.update_yaxes(visible=False)

        value_range = imtool.estimate_range(image)
        image_base64 = imtool.image_encode_base64(image, value_range=value_range)

        self._fig.add_image(source=image_base64,
                            zmax=[value_range, value_range, value_range, value_range])

    def title(self, text: str):
        self._fig.update_layout(title=text)

    def legend(self, show: bool = True):
        self._fig.update_layout(showlegend=show)

    def grid(self, show: bool = True):
        self._fig.update_xaxes(showgrid=show)
        self._fig.update_yaxes(showgrid=show)

    def xlabel(self, text: str):
        self._fig.update_xaxes(title=text)

    def ylabel(self, text: str):
        self._fig.update_yaxes(title=text)

    def xlim(self, min_value: float | None = None,
                   max_value: float | None = None):
        update_axis_limit(figure=self._fig, axis='x', range_min=min_value, range_max=max_value)

    def ylim(self, min_value: float | None = None,
                   max_value: float | None = None):
        update_axis_limit(figure=self._fig, axis='y', range_min=min_value, range_max=max_value)

    def current_color(self) -> str:
        color_name = default_colors_list[self._color_index]
        return default_colors[color_name]

    def scroll_color(self, count: int=1):
        self._color_index += count
        self._color_index %= len(default_colors_list)

    def reset_color(self):
        self._color_index = 0

    def sync_axis_scale(self):
        self._fig.update_yaxes(scaleanchor='x')

    def as_image(self) -> ndarray:
        import io
        from PIL import Image

        fig_bytes = io.BytesIO(self._fig.to_image(format='png'))
        image = Image.open(fig_bytes)
        image = np.asarray(image)
        image = image[..., :3] # RGBA -> RGB
        return image

    def save(self, fname: str):
        import imageio.v3 as iio
        image = self.as_image()
        iio.imwrite(fname, image)

    def close(self):
        self._fig = None

    def show(self, block: bool = False):
        self.engine.pio.show(self._fig)


def update_axis_limit(figure, axis: Literal['x', 'y'],
                      range_min: float | None = None,
                      range_max: float | None = None):
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

    range_min *= 1 - np.sign(range_min) * PlotlyFigure5.RANGE_EXTRA_SPACE_PERCENT / 100
    range_max *= 1 + np.sign(range_max) * PlotlyFigure5.RANGE_EXTRA_SPACE_PERCENT / 100
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