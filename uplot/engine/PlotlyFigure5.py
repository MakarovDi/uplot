from __future__ import annotations

import numpy as np
from numpy import ndarray
from numpy.typing import ArrayLike

import uplot.color as ucolor
import uplot.utool as utool

from uplot.interface import IFigure, LineStyle, MarkerStyle, AspectMode, Colormap
from uplot.engine.PlotlyEngine5 import PlotlyEngine5
from uplot.utool import Interpolator
from uplot.default import DEFAULT


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
        self._color_scroller = ucolor.ColorScroller()

        self._fig: engine.go.Figure = engine.go.Figure()
        self._is_3d = None
        self._colorbar_x_pos = 1.0


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
            # 1.33 - conversion gain between matplotlib and plotly marker size
            marker_size = DEFAULT.marker_size*1.33

        if name is None:
            name = ''
            show_legend = False
        else:
            show_legend = utool.kwargs_extract(kwargs, name='showlegend', default=True)

        if color is None:
            color = self.scroll_color()
        elif not isinstance(color, str):
            # color specified for each point (x, y)
            color = [ ucolor.name_to_hex(c) for c in color]
        else:
            color = ucolor.name_to_hex(color)

        from uplot.engine.plotly import LINE_STYLE_MAPPING, MARKER_STYLE_MAPPING
        line_style = LINE_STYLE_MAPPING[line_style]
        marker_style = MARKER_STYLE_MAPPING[marker_style]

        line = utool.kwargs_extract(kwargs, name='line', default={})
        marker = utool.kwargs_extract(kwargs, name='marker', default={})

        mode = 'lines' if marker_style is None else 'lines+markers'
        if line_style == ' ': # no lines = scatter mode
            mode = 'markers'
            line['dash'] = None
        else:
            line.setdefault('color', color)
            line.setdefault('width', self.engine.LINE_WIDTH)
            line['dash'] = line_style

        marker.setdefault('color', color)
        marker.setdefault('line_color', color)
        marker.setdefault('line_width', self.engine.LINE_WIDTH)
        marker['symbol'] = marker_style
        marker['size'] = marker_size

        hoverlabel = utool.kwargs_extract(kwargs, name='hoverlabel', default={})
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

    def surface3d(self, x            : ArrayLike,
                        y            : ArrayLike,
                        z            : ArrayLike,
                        name         : str | None = None,
                        show_colormap: bool = False,
                        colormap     : Colormap = 'viridis',
                        interpolation: Interpolator = 'cubic',
                        interpolation_range: int = 100,
                        **kwargs):
        x = np.asarray(x)
        y = np.asarray(y)
        z = np.asarray(z)
        assert x.ndim == y.ndim == 1, 'x, y must be 1D arrays'
        assert z.ndim == 1 or z.ndim == 2, 'z must be 1D or 2D array'

        if z.ndim == 2:
            # uniform grid
            assert (len(y), len(x)) == z.shape, 'uniform grid: x and y range must match z'
            x, y = np.meshgrid(x, y)
        else:
            # non-uniform grid - array of points (x, y, z)
            x, y, z = utool.array_to_grid(x, y, z,
                                          interpolation=interpolation,
                                          interpolation_range=interpolation_range)

        self._is_3d = True

        if show_colormap:
            colorbar = dict(len=0.5, x=self._colorbar_x_pos)
            self._colorbar_x_pos += 0.12
        else:
            colorbar = None

        self._fig.add_surface(x=x, y=y, z=z,
                              name=name,
                              showlegend=(name != '') and (name is not None),
                              showscale=show_colormap,
                              colorscale=colormap,
                              colorbar=colorbar,
                              **kwargs)


    def imshow(self, image: ArrayLike, **kwargs):
        image = np.asarray(image)
        value_range = utool.image_range(image)

        self._is_3d = False

        self._fig.add_trace(self.engine.go.Image(
            z=image,
            zmax=utool.kwargs_extract(kwargs, name='zmax', default=[value_range]*4),
            zmin=utool.kwargs_extract(kwargs, name='zmin', default=[0]*4),
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
            bgcolor=utool.kwargs_extract(kwargs, name='bgcolor', default='rgba(255,255,255,0.8)'),
            itemsizing=utool.kwargs_extract(kwargs, name='itemsizing', default='constant'),
            itemwidth=utool.kwargs_extract(kwargs, name='itemwidth', default=50),
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
        return self._color_scroller.current_color()

    def scroll_color(self, count: int=1) -> str:
        return self._color_scroller.scroll_color(count)

    def reset_color(self):
        self._color_scroller.reset()

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

    def save(self, filename: str):
        if '.html' in filename:
            self._fig.write_html(filename)
        else:
            self._fig.write_image(filename)

    def close(self):
        self._fig = None

    def show(self, block: bool=True):
        self.engine.pio.show(self._fig)