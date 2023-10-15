from __future__ import annotations

import numpy as np
from numpy import ndarray
from numpy.typing import ArrayLike

import uplot.imtool as imtool

from uplot.interface import IFigure, LineStyle, MarkerStyle
from uplot.engine.MatplotEngine import MatplotEngine
from uplot.colors import default_colors_list, decode_color, default_colors
from uplot.routine import unpack_param, kwargs_extract


class MatplotFigure(IFigure):

    @property
    def engine(self) -> MatplotEngine:
        return self._engine

    @property
    def internal(self):
        return self._fig


    def __init__(self, engine: MatplotEngine):
        self._engine = engine

        self._fig: engine.plt.Figure = engine.plt.figure(dpi=engine.SHOWING_DPI, layout='constrained')
        self._axis: engine.plt.Axes = self._fig.gca()
        # Constrained layout automatically adjusts subplots so that decorations like tick labels,
        # legends, and colorbars do not overlap, while still preserving the logical layout requested by the user.
        # Constrained layout is similar to Tight layout, but is substantially more flexible.
        # https://matplotlib.org/stable/users/explain/axes/constrainedlayout_guide.html

        self._color_index = 0

        # default style
        self._axis.grid(visible=True)

    def plot(self,
             x           : ArrayLike,
             y           : ArrayLike | None = None,
             name        : str | list[str] | None = None,
             color       : str | list[str] | None = None,
             line_style  : LineStyle | list[LineStyle] | None = None,
             marker_style: MarkerStyle | list[MarkerStyle] | None = None,
             marker_size : int | None = None,
             opacity     : float = 1.0,
             **kwargs):
        x = np.atleast_1d(np.asarray(x))

        if y is not None:
            y = np.asarray(y)
        else:
            y = x
            x = np.arange(len(y))

        y = y.reshape([len(x), -1])

        if marker_size is None:
            marker_size = self.engine.MARKER_SIZE

        for i, y_i in enumerate(y.T):
            color_i = decode_color(unpack_param(color, i))
            name_i = unpack_param(name, i)
            marker_i = unpack_param(marker_style, i)
            line_i = unpack_param(line_style, i)

            if color_i is None:
                color_i = self.current_color()
                self.scroll_color()

            if line_i == ' ':
                self._axis.scatter(x, y_i,
                                   color=color_i,
                                   label=name_i,
                                   marker=marker_i,
                                   s=marker_size**2,
                                   alpha=opacity,
                                   **kwargs)
            else:
                self._axis.plot(x, y_i,
                                color=color_i,
                                label=name_i,
                                marker=marker_i,
                                linestyle=line_i,
                                markersize=marker_size,
                                alpha=opacity,
                                **kwargs)

    def scatter(self,
                x           : ArrayLike,
                y           : ArrayLike | None = None,
                name        : str | list[str] | None = None,
                color       : str | list[str] | None = None,
                marker_style: MarkerStyle | list[MarkerStyle] | None = None,
                marker_size : int | None = None,
                opacity     : float = 1.0,
                **kwargs):
        self.plot(x=x, y=y,
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

    def xlim(self, min_value: float | None = None,
                   max_value: float | None = None):
        self._axis.set_xlim(left=min_value, right=max_value)

    def ylim(self, min_value: float | None = None,
                   max_value: float | None = None):
        self._axis.set_ylim(bottom=min_value, top=max_value)

    def current_color(self) -> str:
        color_name = default_colors_list[self._color_index]
        return default_colors[color_name]

    def scroll_color(self, count: int=1):
        self._color_index += count
        self._color_index %= len(default_colors_list)

    def reset_color(self):
        self._color_index = 0

    def sync_axis_scale(self):
        w, h = self._fig.get_size_inches()
        mx = max(w, h)
        self._fig.set_size_inches(mx, mx)

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
            # but not the best, probably (because it'll show all figures).
            self.engine.plt.show()
            return

        if not self.engine.is_gui_backend:
            # no need to show, bypass
            return

        # show only this figure
        self._fig.show()
        if block:
            self._fig.waitforbuttonpress()