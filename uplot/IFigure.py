from typing import Protocol
from numpy.typing import ArrayLike
from numpy import ndarray

from uplot.LineStyle import LineStyle
from uplot.MarkerStyle import MarkerStyle


class IFigure(Protocol):

    def plot(self, x          : ArrayLike,
                   y          : ArrayLike | None = None,
                   name       : str | list[str] | None = None,
                   color      : str | list[str] | None = None,
                   line       : LineStyle | list[LineStyle] | None = None,
                   marker     : MarkerStyle | list[MarkerStyle] | None = None,
                   marker_size: int | None = None,
                   opacity    : float = 1.0):
        pass

    def scatter(self, x          : ArrayLike,
                      y          : ArrayLike | None = None,
                      name       : str | list[str] | None = None,
                      color      : str | list[str] | None = None,
                      marker     : MarkerStyle | list[MarkerStyle] | None = None,
                      marker_size: int | None = None,
                      opacity    : float = 1.0):
        pass

    def imshow(self, image: ArrayLike):
        pass

    def title(self, text: str):
        pass

    def legend(self, show: bool = True):
        pass

    def grid(self, show: bool = True):
        pass

    def xlabel(self, text: str):
        pass

    def ylabel(self, text: str):
        pass

    def xlim(max_value: float | None = None,
             min_value: float | None = None):
        pass

    def ylim(max_value: float | None = None,
             min_value: float | None = None):
        pass

    def current_color(self) -> str:
        pass

    def scroll_color(self, count: int=1):
        pass

    def reset_color(self):
        pass

    def sync_axix_scale():
        pass

    def as_image(self) -> ndarray:
        pass

    def save(self, fname: str):
        pass

    def close(self):
        pass

    def show(self):
        pass