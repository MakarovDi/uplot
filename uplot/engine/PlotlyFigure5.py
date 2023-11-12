from __future__ import annotations

import numpy as np
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
            show_legend = kwargs_extract(kwargs, name='showlegend', default=True)

        if color is None:
            color = self.current_color()
            self.scroll_color()
        elif not isinstance(color, str):
            # color specified for each point (x, y)
            color = [ decode_color(c) for c in color ]
        else:
            color = decode_color(color)

        from uplot.engine.plotly import LINE_STYLE_MAPPING, MARKER_STYLE_MAPPING
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
            line.setdefault('width', self.engine.LINE_WIDTH)

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
                                  hoverlabel=hoverlabel,
                                  **kwargs)
        else:
            self._fig.add_scatter3d(x=x, y=y, z=z,
                                    name=name,
                                    mode=mode,
                                    line=line,
                                    marker=marker,
                                    opacity=opacity,
                                    showlegend=show_legend,
                                    hoverlabel=hoverlabel,
                                    **kwargs)

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
        if self.is_3d:
            self._fig.update_layout(scene=dict(xaxis_title=text))
        else:
            self._fig.update_xaxes(title=text)

    def ylabel(self, text: str):
        if self.is_3d:
            self._fig.update_layout(scene=dict(yaxis_title=text))
        else:
            self._fig.update_yaxes(title=text)

    def zlabel(self, text: str):
        if self.is_3d:
            self._fig.update_layout(scene=dict(zaxis_title=text))

    def xlim(self, min_value: float | None = None,
                   max_value: float | None = None):
        from uplot.engine.plotly import estimate_axis_range

        if min_value is None:
            min_value = estimate_axis_range(self._fig, axis='x', mode='min')
        if max_value is None:
            max_value = estimate_axis_range(self._fig, axis='x', mode='max')
        if self.is_3d:
            self._fig.update_layout(scene=dict(xaxis=dict(range=[min_value, max_value])))
        else:
            self._fig.update_xaxes(range=[min_value, max_value])

    def ylim(self, min_value: float | None = None,
                   max_value: float | None = None):
        from uplot.engine.plotly import estimate_axis_range

        if min_value is None:
            min_value = estimate_axis_range(self._fig, axis='y', mode='min')
        if max_value is None:
            max_value = estimate_axis_range(self._fig, axis='y', mode='max')

        if self.is_3d:
            self._fig.update_layout(scene=dict(yaxis=dict(range=[min_value, max_value])))
        else:
            self._fig.update_yaxes(range=[min_value, max_value])

    def zlim(self, min_value: float | None = None,
                   max_value: float | None = None):
        if not self.is_3d:
            return

        from uplot.engine.plotly import estimate_axis_range

        if min_value is None:
            min_value = estimate_axis_range(self._fig, axis='z', mode='min')
        if max_value is None:
            max_value = estimate_axis_range(self._fig, axis='z', mode='max')

        self._fig.update_layout(scene=dict(zaxis=dict(range=[min_value, max_value])))

    def current_color(self) -> str:
        color_name = default_colors_list[self._color_index]
        return default_colors[color_name]

    def scroll_color(self, count: int=1):
        self._color_index += count
        self._color_index %= len(default_colors_list)

    def reset_color(self):
        self._color_index = 0

    def axis_aspect(self, mode: AspectMode):
        if self.is_3d:
            if mode == AspectMode.EQUAL:
                aspectmode = 'cube' if mode == AspectMode.EQUAL else 'auto'
                self._fig.update_scenes(aspectmode=aspectmode)
        else:
            scaleanchor = 'x' if mode == AspectMode.EQUAL else None
            self._fig.update_yaxes(scaleanchor=scaleanchor)

    def as_image(self) -> ndarray:
        import io
        from PIL import Image

        fig_bytes = io.BytesIO(
            self._fig.to_image(format='png', scale=self.engine.FILE_RESOLUTION_SCALE)
        )

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

    def show(self, block: bool=True):
        self.engine.pio.show(self._fig)