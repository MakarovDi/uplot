from __future__ import annotations

import numpy as np
from numpy import ndarray
from numpy.typing import ArrayLike

import uplot.imtool as imtool

from uplot.interface import IFigure, LineStyle, MarkerStyle, AspectMode
from uplot.engine.MatplotEngine import MatplotEngine
from uplot.color import default_colors_list, decode_color, default_colors
from uplot.routine import kwargs_extract


class MatplotFigure(IFigure):

    @property
    def engine(self) -> MatplotEngine:
        return self._engine

    @property
    def internal(self):
        return self._fig

    @property
    def is_3d(self) -> bool | None:
        return self._is_3d

    def __init__(self, engine: MatplotEngine, width: int, aspect_ratio: float):
        self._engine = engine
        self._is_3d = None
        self._axis: engine.plt.Axes = None

        # temporary styling (no global effect):
        # https://matplotlib.org/stable/users/explain/customizing.html
        with engine.plt.style.context(engine.STYLE):
            self._fig: engine.plt.Figure = engine.plt.figure(dpi=engine.SHOWING_DPI, layout='constrained')
            # Constrained layout automatically adjusts subplots so that decorations like tick labels,
            # legends, and colorbars do not overlap, while still preserving the logical layout requested by the user.
            # Constrained layout is similar to Tight layout, but is substantially more flexible.
            # https://matplotlib.org/stable/users/explain/axes/constrainedlayout_guide.html
            self._fig.set_figwidth(width / engine.SHOWING_DPI)
            self._fig.set_figheight(aspect_ratio*(width / engine.SHOWING_DPI))

        self._color_index = 0

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

        if z is None: # 2d
            self._init_axis(is_3d=False)
        else: # 3d
            z = np.atleast_1d(np.asarray(z))
            assert z.ndim == 1, 'the input must be 1d arrays'
            assert len(x) == len(z), 'the length of the input arrays must be the same'
            self._init_axis(is_3d=True)

        if marker_size is None:
            marker_size = self.engine.MARKER_SIZE

        if color is None:
            color = self.current_color()
            self.scroll_color()
        elif color is not isinstance(color, str):
            # color specified for each point (x, y)
            color = [ decode_color(c) for c in color ]
        else:
            color = decode_color(color)

        if self.is_3d:
            plot_data = x, y, z
        else:
            plot_data = x, y

        if line_style == ' ': # only markers
            self._axis.scatter(*plot_data,
                               color=color,
                               label=name,
                               marker=marker_style,
                               s=marker_size**2,
                               alpha=opacity,
                               **kwargs)
        else:
            self._axis.plot(*plot_data,
                            color=color,
                            label=name,
                            marker=marker_style,
                            markersize=marker_size,
                            linestyle=line_style,
                            alpha=opacity,
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

        self._init_axis(is_3d=False)
        self._axis.imshow(image / value_range,
                          cmap=kwargs_extract(kwargs, name='cmap', default=self.engine.plt.get_cmap('gray')),
                          vmin=kwargs_extract(kwargs, name='vmin', default=0),
                          vmax=kwargs_extract(kwargs, name='vmax', default=1.0),
                          interpolation=kwargs_extract(kwargs, name='interpolation', default='none')
        )

        # hide grid, frame, ticks and labels
        self._axis.grid(visible=False)
        self._axis.get_xaxis().set_visible(False)
        self._axis.get_yaxis().set_visible(False)
        self._axis.set_frame_on(False)

    def title(self, text: str):
        self._axis.set_title(label=text)

    def legend(self, show: bool = True, **kwargs):
        handles, labels = self._axis.get_legend_handles_labels()
        if len(handles) > 0:
            loc = kwargs_extract(kwargs, name='loc', default='outside right upper')
            if 'outside' in loc:
                # outside works only for the figure
                # "outside right upper" works correctly with "constrained" or "compressed" layout only
                self._fig.legend().set(visible=show, loc=loc, **kwargs)
            else:
                # axes.legend() is better for an other options because legend will be inside graph
                self._fig.gca().legend().set(visible=show, loc=loc, **kwargs)

    def grid(self, show: bool = True):
        self._axis.grid(visible=show)

    def xlabel(self, text: str):
        self._axis.set_xlabel(xlabel=text)

    def ylabel(self, text: str):
        self._axis.set_ylabel(ylabel=text)

    def zlabel(self, text: str):
        if self.is_3d:
            self._axis.set_zlabel(zlabel=text)

    def xlim(self, min_value: float | None = None,
                   max_value: float | None = None):
        self._axis.set_xlim(left=min_value, right=max_value)

    def ylim(self, min_value: float | None = None,
                   max_value: float | None = None):
        self._axis.set_ylim(bottom=min_value, top=max_value)

    def zlim(self, min_value: float | None = None,
                   max_value: float | None = None):
        if self.is_3d:
            self._axis.set_zlim(bottom=min_value, top=max_value)

    def current_color(self) -> str:
        color_name = default_colors_list[self._color_index]
        return default_colors[color_name]

    def scroll_color(self, count: int=1):
        self._color_index += count
        self._color_index %= len(default_colors_list)

    def reset_color(self):
        self._color_index = 0

    def axis_aspect(self, mode: AspectMode):
        # https://stackoverflow.com/questions/8130823/set-matplotlib-3d-plot-aspect-ratio
        self._axis.set_aspect(aspect=mode)

    def as_image(self) -> ndarray:
        fig = self._fig

        fig.set_dpi(self.engine.SAVING_DPI)

        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)

        w, h = fig.canvas.get_width_height()
        return image.reshape([h, w, 3])

    def save(self, fname: str):
        self._fig.savefig(fname, dpi=self.engine.SAVING_DPI)

    def close(self):
        self._fig.close()
        self._fig = None

    def show(self, block: bool = False):
        if self.engine.is_ipython_backend:
            # There are two ways for consistent figure visualization in jupyter
            #    1. call `%matplotlib ...` at the notebook start.
            #    2. always use `plt.show()`.
            # It's easy to forget about (1) so `plt.show()` is more reliable
            # but not the best, probably (because it will show all figures).
            self.engine.plt.show()
            return

        if not self.engine.is_gui_backend:
            return # no need to show, bypass

        self._fig.show() # show only this figure

        if block:
            while self.engine.plt.fignum_exists(self._fig.number):
                # allow multiple mouse clicks for 3d plot manipulation
                self._fig.waitforbuttonpress()


    def _init_axis(self, is_3d: bool):
        if self.is_3d == is_3d:
            # axis already initialized
            return

        # remove current axis
        self._fig.clear()

        # temporary styling (no global effect):
        with self.engine.plt.style.context(self.engine.STYLE):
            projection = '3d' if is_3d else None
            self._axis = self._fig.add_subplot(projection=projection)

        self._is_3d = is_3d
        self._axis.grid(visible=True) # show grid by default

        if is_3d:
            # sync axis and figure color
            self._axis.set_facecolor(self._fig.get_facecolor())