from __future__ import annotations

import numpy as np
from numpy import ndarray
from numpy.typing import ArrayLike
from typing import Any

import uplot.color as ucolor
import uplot.utool as utool
import uplot.plugin as plugin

from uplot.interface import IFigure, LineStyle, MarkerStyle, AspectMode, Colormap
from uplot.engine.MatplotEngine import MatplotEngine
from uplot.utool import Interpolator
from uplot.default import DEFAULT


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
        with engine.plt.style.context(DEFAULT.style):
            self._fig: engine.plt.Figure = engine.plt.figure(dpi=engine.SHOWING_DPI, layout='constrained')
            # constrained layout automatically adjusts subplots so that decorations like tick labels,
            # legends, and colorbars do not overlap, while still preserving the logical layout requested by the user.
            # constrained layout is similar to Tight layout, but is substantially more flexible.
            # https://matplotlib.org/stable/users/explain/axes/constrainedlayout_guide.html
            self._fig.set_figwidth(width / engine.SHOWING_DPI)
            self._fig.set_figheight(aspect_ratio*(width / engine.SHOWING_DPI))

        self._color_scroller = ucolor.ColorScroller()
        self._init_axis(is_3d=False)

    def plot(self, x           : ArrayLike,
                   y           : ArrayLike | None = None,
                   z           : ArrayLike | None = None,
                   name        : str | None = None,
                   color       : str | None = None,
                   line_style  : LineStyle | None = None,
                   marker_style: MarkerStyle | None = None,
                   marker_size : int | None = None,
                   opacity     : float = 1.0,
                   legend_group: str | None = None,
                   **kwargs) -> IFigure:
        from uplot.engine.matplot.plot import plot_line_marker

        # check if x is a custom object and a plugin is available
        if plugin.plot(plot_method=self.plot,
                       x=x, y=y, z=z,
                       name=name,
                       color=color,
                       line_style=line_style,
                       marker_style=marker_style,
                       marker_size=marker_size,
                       opacity=opacity,
                       legend_group=legend_group,
                       **kwargs):
            return self

        # get or init axis
        axis = self._init_axis(is_3d=z is not None)

        # init color
        if color is None:
            color = self.scroll_color()

        plot_line_marker(axis=axis,
                         x=x, y=y, z=z,
                         name=name,
                         color=color,
                         line_style=line_style,
                         marker_style=marker_style,
                         marker_size=marker_size,
                         opacity=opacity,
                         **kwargs)
        return self

    def scatter(self, x           : ArrayLike,
                      y           : ArrayLike | None = None,
                      z           : ArrayLike | None = None,
                      name        : str | None = None,
                      color       : str | list[str] | None = None,
                      marker_style: MarkerStyle | None = None,
                      marker_size : int | None = None,
                      opacity     : float = 1.0,
                      legend_group: str | None = None,
                      **kwargs) -> IFigure:
        from uplot.engine.matplot.plot import plot_line_marker

        # check if x is a custom object and a plugin is available
        if plugin.plot(plot_method=self.scatter,
                       x=x, y=y, z=z,
                       name=name,
                       color=color,
                       marker_style=marker_style,
                       marker_size=marker_size,
                       opacity=opacity,
                       legend_group=legend_group,
                       **kwargs):
            return self

        # get or init axis
        axis = self._init_axis(is_3d=z is not None)

        # init color
        if color is None:
            color = self.scroll_color()

        plot_line_marker(axis=axis,
                         x=x, y=y, z=z,
                         name=name,
                         color=color,
                         line_style=' ',  # no line (scatter mode)
                         marker_style=marker_style,
                         marker_size=marker_size,
                         opacity=opacity,
                         **kwargs)
        return self

    def hline(self, y           : float,
                    x_min       : float | None = None,
                    x_max       : float | None = None,
                    name        : str | None = None,
                    color       : str | None = None,
                    line_style  : LineStyle | None = None,
                    opacity     : float = 1.0,
                    legend_group: str | None = None,
                    **kwargs) -> IFigure:

        if self.is_3d:
            raise RuntimeError('3D figure is not supported')

        if x_min is None:
            x_min, _ = self._axis.get_xlim()

        if x_max is None:
            _, x_max = self._axis.get_xlim()

        return self.plot([x_min, x_max], [y, y],
                         color=color,
                         name=name,
                         line_style=line_style,
                         opacity=opacity,
                         legend_group=legend_group,
                         **kwargs)

    def vline(self, x           : float,
                    y_min       : float | None = None,
                    y_max       : float | None = None,
                    name        : str | None = None,
                    color       : str | None = None,
                    line_style  : LineStyle | None = None,
                    opacity     : float = 1.0,
                    legend_group: str | None = None,
                    **kwargs) -> IFigure:
        if self.is_3d:
            raise RuntimeError('3D figure is not supported')

        if y_min is None:
            y_min, _ = self._axis.get_ylim()

        if y_max is None:
            _, y_max = self._axis.get_ylim()

        return self.plot([x, x], [y_min, y_max],
                         color=color,
                         name=name,
                         line_style=line_style,
                         opacity=opacity,
                         legend_group=legend_group,
                         **kwargs)

    def surface3d(self, x            : ArrayLike | Any,
                        y            : ArrayLike | None = None,
                        z            : ArrayLike | None = None,
                        name         : str | None = None,
                        show_colormap: bool = False,
                        colormap     : Colormap = 'viridis',
                        opacity      : float = 1.0,
                        interpolation: Interpolator = 'cubic',
                        interpolation_range: int = 100,
                        legend_group : str | None = None,
                        **kwargs) -> IFigure:
        # check if x is a custom object and a plugin is available
        if plugin.plot(plot_method=self.surface3d,
                       x=x, y=y, z=z,
                       name=name,
                       show_colormap=show_colormap,
                       colormap=colormap,
                       opacity=opacity,
                       interpolation=interpolation,
                       interpolation_range=interpolation_range,
                       legend_group=legend_group,
                       **kwargs):
            return self

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

        axis = self._init_axis(is_3d=True)

        cmap = self.engine.mpl.colormaps[colormap.lower()]

        surf = axis.plot_surface(x, y, z,
                                 label=name,
                                 cmap=cmap,
                                 # antialiased=False: to fix some of z-order issues (not all of them)
                                 # https://stackoverflow.com/questions/39144482/matplotlib-plot-surface-transparency-artefact
                                 antialiased=False,
                                 alpha=opacity,
                                 **kwargs)
        if show_colormap:
            self._fig.colorbar(surf, shrink=0.5, aspect=10)

        return self

    def imshow(self, image: ArrayLike, **kwargs) -> IFigure:
        image = np.asarray(image)

        if 'vmin' in kwargs or 'vmax' in kwargs:
            # fallback to matplotlib behaviour if
            # the image range provided directly
            vmin = kwargs.pop('vmin', None)
            vmax = kwargs.pop('vmax', None)
        else:
            # test the image for type and convert to [0, 1] range
            image = image / utool.image_range(image)
            vmin = 0.0
            vmax = 1.0

        axis = self._init_axis(is_3d=False)
        axis.imshow(image,
            cmap=kwargs.pop('cmap', self.engine.plt.get_cmap('gray')),
            vmin=vmin, vmax=vmax,
            interpolation=kwargs.pop('interpolation', 'none')
        )

        # hide grid, frame, ticks and labels
        axis.grid(visible=False)
        axis.get_xaxis().set_visible(False)
        axis.get_yaxis().set_visible(False)
        axis.set_frame_on(False)

        return self

    def title(self, text: str) -> IFigure:
        self._axis.set_title(label=text)
        return self

    def legend(self, show: bool = True,
                     equal_marker_size: bool = True,
                     **kwargs) -> IFigure:
        if not self._axis:
            return self

        # check if there is anything to put to the legend
        handles, labels = self._axis.get_legend_handles_labels()
        if len(handles) == 0:
            return self

        if equal_marker_size:
            from matplotlib.legend_handler import HandlerPathCollection, HandlerLine2D
            from matplotlib.collections import PathCollection
            from matplotlib.pyplot import Line2D

            def updatescatter(handle, orig):
                handle.update_from(orig)
                handle.set_sizes([self.engine.LEGEND_MARKER_SIZE ** 2])
            def updateline(handle, orig):
                handle.update_from(orig)
                handle.set_markersize(self.engine.LEGEND_MARKER_SIZE)

            handler_map = { PathCollection: HandlerPathCollection(update_func=updatescatter),
                            Line2D: HandlerLine2D(update_func=updateline) }
        else:
            handler_map = None

        if not show:
            self._fig.legends.clear() # remove legend outside axis
            self._fig.gca().legend().remove() # remove legend inside
            return self

        # create legend
        loc = kwargs.pop('loc', 'outside right upper')
        if 'outside' in loc:
            # outside works only for the figure
            # "outside right upper" works correctly with "constrained" or "compressed" layout only
            self._fig.legend(handler_map=handler_map).set(loc=loc, **kwargs)
        else:
            # axes.legend() is better for an other options because legend will be inside the graph
            self._fig.gca().legend(handler_map=handler_map).set(loc=loc, **kwargs)

        return self

    def grid(self, show: bool = True) -> IFigure:
        self._axis.grid(visible=show)
        return self

    def xlabel(self, text: str) -> IFigure:
        self._axis.set_xlabel(xlabel=text)
        return self

    def ylabel(self, text: str) -> IFigure:
        self._axis.set_ylabel(ylabel=text)
        return self

    def zlabel(self, text: str) -> IFigure:
        if self.is_3d:
            self._axis.set_zlabel(zlabel=text)
        return self

    def xlim(self, min_value: float | None = None,
                   max_value: float | None = None) -> IFigure:
        self._axis.set_xlim(left=min_value, right=max_value)
        return self

    def ylim(self, min_value: float | None = None,
                   max_value: float | None = None) -> IFigure:
        self._axis.set_ylim(bottom=min_value, top=max_value)
        return self

    def zlim(self, min_value: float | None = None,
                   max_value: float | None = None) -> IFigure:
        if self.is_3d:
            self._axis.set_zlim(bottom=min_value, top=max_value)
        return self

    def current_color(self) -> str:
        return self._color_scroller.current_color()

    def scroll_color(self, count: int=1) -> str:
        return self._color_scroller.scroll_color(count)

    def reset_color(self) -> IFigure:
        self._color_scroller.reset()
        return self

    def axis_aspect(self, mode: AspectMode) -> IFigure:
        # https://stackoverflow.com/questions/8130823/set-matplotlib-3d-plot-aspect-ratio
        self._axis.set_aspect(aspect=mode)
        return self

    def as_image(self) -> ndarray:
        fig = self._fig

        fig.set_dpi(self.engine.SAVING_DPI)

        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)

        w, h = fig.canvas.get_width_height()
        return image.reshape([h, w, 3])

    def save(self, filename: str):
        self._fig.savefig(filename, dpi=self.engine.SAVING_DPI)

    def close(self):
        self.engine.plt.close(self._fig)
        self._fig = None

    def show(self, block: bool=True):
        if self.engine.is_ipython_backend:
            # there are two ways for consistent figure visualization in jupyter
            #    1. call `%matplotlib ...` at the notebook start.
            #    2. always use `plt.show()`.
            # it's easy to forget about (1) so `plt.show()` is more reliable
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
            return self._axis

        # remove current axis
        self._fig.clear()

        # temporary styling (no global effect):
        with self.engine.plt.style.context(DEFAULT.style):
            projection = '3d' if is_3d else None
            self._axis = self._fig.add_subplot(projection=projection)

        self._is_3d = is_3d
        self._axis.grid(visible=True) # show grid by default

        if is_3d:
            # sync axis and figure color
            self._axis.set_facecolor(self._fig.get_facecolor())

        return self._axis