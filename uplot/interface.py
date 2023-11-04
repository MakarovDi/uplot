from __future__ import annotations

from numpy import ndarray
from typing import Protocol, runtime_checkable
from abc import abstractmethod as abstract
from numpy.typing import ArrayLike

from uplot.LineStyle import LineStyle
from uplot.MarkerStyle import MarkerStyle
from uplot.AspectMode import AspectMode

# TODO: documentation

@runtime_checkable
class IFigure(Protocol):
    """
    Matplotlib-like interface for plotting.

    Note
    ----
    Probably it's not the best choice of the interface
    but very common and familiar for MATLAB users.
    """
    @property
    @abstract
    def engine(self) -> IPlotEngine:
        return ...

    @property
    @abstract
    def internal(self):
        return ...

    @property
    @abstract
    def is_3d(self) -> bool:
        return ...

    @abstract
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
        ...

    @abstract
    def scatter(self, x           : ArrayLike,
                      y           : ArrayLike | None = None,
                      z           : ArrayLike | None = None,
                      name        : str | None = None,
                      color       : str | list[str] | None = None,
                      marker_style: MarkerStyle | list[MarkerStyle] | None = None,
                      marker_size : int | None = None,
                      opacity     : float = 1.0,
                      **kwargs):
        ...

    @abstract
    def imshow(self, image: ArrayLike, **kwargs):
        ...

    @abstract
    def title(self, text: str):
        ...

    @abstract
    def legend(self, show: bool = True, **kwargs):
        ...

    @abstract
    def grid(self, show: bool = True):
        ...

    @abstract
    def xlabel(self, text: str):
        ...

    @abstract
    def ylabel(self, text: str):
        ...

    @abstract
    def zlabel(self, text: str):
        ...

    @abstract
    def xlim(self, min_value: float | None = None,
                   max_value: float | None = None):
        ...

    @abstract
    def ylim(self, min_value: float | None = None,
                   max_value: float | None = None):
        ...

    @abstract
    def zlim(self, min_value: float | None = None,
                   max_value: float | None = None):
        ...

    @abstract
    def current_color(self) -> str:
        ...

    @abstract
    def scroll_color(self, count: int = 1):
        ...

    @abstract
    def reset_color(self):
        ...

    @abstract
    def axis_aspect(self, mode: AspectMode):
        ...

    @abstract
    def as_image(self) -> ndarray:
        ...

    @abstract
    def save(self, fname: str):
        ...

    @abstract
    def close(self):
        ...

    @abstract
    def show(self, block: bool = False):
        ...

@runtime_checkable
class IPlotEngine(Protocol):

    @classmethod
    @abstract
    def is_available(cls) -> bool:
        ...

    @property
    @abstract
    def figure_type(self) -> type:
        return ...

    @abstract
    def figure(self, width: int, aspect_ratio: float) -> IFigure:
        """
        Factory method for a figure creation
        """
        ...