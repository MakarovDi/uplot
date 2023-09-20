from __future__ import annotations

import numpy as np
from numpy import ndarray
from numpy.typing import ArrayLike

import uplot.imtool as imtool

from uplot.interface import IFigure, LineStyle, MarkerStyle
from uplot.engine.MatplotEngine import MatplotEngine
from uplot.colors import default_colors_list, decode_color, default_colors
from uplot.routine import unpack_param


class MatplotFigure(IFigure):
    DEFAULT_MARKER_SIZE = 6
    DEFAULT_SHOWING_DPI = 150
    DEFAULT_SAVING_DPI = 300

    @property
    def engine(self) -> MatplotEngine:
        return self._engine

    @property
    def internal(self):
        return self._fig


    def __init__(self, engine: MatplotEngine):
        self._engine = engine

        self._fig: engine.plt.Figure = engine.plt.figure(dpi=self.DEFAULT_SHOWING_DPI)
        self._axis: engine.plt.Axes = self._fig.gca()

        self._legend_visible = False
        self._color_index = 0

        # default style
        self._fig.tight_layout(pad=2.8)
        self._axis.grid(visible=True)

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

        if marker_size is None:
            marker_size = self.DEFAULT_MARKER_SIZE

        y = y.reshape([len(x), -1])

        for i, y_i in enumerate(y.T):
            color_i = decode_color(unpack_param(color, i))
            name_i = unpack_param(name, i)
            marker_i = unpack_param(marker, i)
            line_i = unpack_param(line, i)

            if color_i is None:
                color_i = self.current_color()
                self.scroll_color()

            if line_i == ' ':
                self._axis.scatter(x, y_i,
                                   color=color_i,
                                   label=name_i,
                                   marker=marker_i,
                                   s=marker_size**2,
                                   alpha=opacity)
            else:
                self._axis.plot(x, y_i,
                                color=color_i,
                                label=name_i,
                                marker=marker_i,
                                linestyle=line_i,
                                markersize=marker_size,
                                alpha=opacity)

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
        value_range = imtool.estimate_range(image)
        self._axis.grid(visible=False)
        self._axis.imshow(image / value_range,
                          cmap=self.engine.plt.get_cmap('gray'),
                          vmin=0, vmax=1.0,
                          interpolation='none')

    def title(self, text: str):
        self._axis.set_title(label=text)

    def legend(self, show: bool = True):
        handles, labels = self._axis.get_legend_handles_labels()
        if len(handles) > 0:
            self._axis.legend(handles, labels).set_visible(show)
            self._legend_visible = show

    def grid(self, show: bool = True):
        self._axis.grid(visible=show)

    def xlabel(self, text: str):
        self._axis.set_xlabel(xlabel=text)

    def ylabel(self, text: str):
        self._axis.set_ylabel(ylabel=text)

    def xlim(self, min_value: float | None = None,
                   max_value: float | None = None):
        self._axis.set_xlim(left=min_value, right=max_value) # type: ignore # matplotlib incomplete annotation

    def ylim(self, min_value: float | None = None,
                   max_value: float | None = None):
        self._axis.set_ylim(bottom=min_value, top=max_value) # type: ignore # matplotlib incomplete annotation

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
        fig.set_dpi(self.DEFAULT_SAVING_DPI)

        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)

        w, h = fig.canvas.get_width_height()
        return image.reshape([h, w, 3])

    def save(self, fname: str):
        self._fig.savefig(fname, dpi=self.DEFAULT_SAVING_DPI)

    def close(self):
        self._fig.close()
        self._fig = None

    def show(self, block: bool = False):
        if not self.engine.is_gui_backend:
            # not possible to show
            return

        self._fig.show()
        if block:
            self._fig.waitforbuttonpress()