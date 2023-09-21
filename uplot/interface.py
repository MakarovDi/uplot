from __future__ import annotations

from numpy import ndarray
from typing import Protocol, runtime_checkable
from numpy.typing import ArrayLike

from uplot.LineStyle import LineStyle
from uplot.MarkerStyle import MarkerStyle

# TODO: documentation

class IFigure(Protocol):
    """
    Matplotlib-like interface for plotting.

    Note
    ----
    Probably it's not the best choice of the interface
    but very common and familiar for MATLAB users.
    """
    @property
    def engine(self) -> IPlotEngine:
        return ...

    @property
    def internal(self):
        return ...

    def plot(self, x          : ArrayLike,
                   y          : ArrayLike | None = None,
                   name       : str | list[str] | None = None,
                   color      : str | list[str] | None = None,
                   line       : LineStyle | list[LineStyle] | None = None,
                   marker     : MarkerStyle | list[MarkerStyle] | None = None,
                   marker_size: int | None = None,
                   opacity    : float = 1.0):
        ...

    def scatter(self, x          : ArrayLike,
                      y          : ArrayLike | None = None,
                      name       : str | list[str] | None = None,
                      color      : str | list[str] | None = None,
                      marker     : MarkerStyle | list[MarkerStyle] | None = None,
                      marker_size: int | None = None,
                      opacity    : float = 1.0):
        ...

    def imshow(self, image: ArrayLike):
        ...

    def title(self, text: str):
        ...

    def legend(self, show: bool = True):
        ...

    def grid(self, show: bool = True):
        ...

    def xlabel(self, text: str):
        ...

    def ylabel(self, text: str):
        ...

    def xlim(self, min_value: float | None = None,
                   max_value: float | None = None):
        ...

    def ylim(self, min_value: float | None = None,
                   max_value: float | None = None):
        ...

    def current_color(self) -> str:
        ...

    def scroll_color(self, count: int = 1):
        ...

    def reset_color(self):
        ...

    def sync_axis_scale(self):
        ...

    def as_image(self) -> ndarray:
        ...

    def save(self, fname: str):
        ...

    def close(self):
        ...

    def show(self, block: bool = False):
        ...

@runtime_checkable
class IPlotEngine(Protocol):

    @classmethod
    def is_available(cls) -> bool:
        ...

    @property
    def figure_type(self) -> type:
        return ...

    def figure(self, aspect_ratio: float) -> IFigure:
        """
        Factory method for a figure creation
        """
        ...