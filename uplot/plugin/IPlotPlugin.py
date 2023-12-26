from typing import Any, NamedTuple
from abc import abstractmethod as abstract
from numpy.typing import ArrayLike


class PlotData(NamedTuple):
    x: ArrayLike
    y: ArrayLike
    z: ArrayLike | None = None
    name: str | None = None


class IPlotPlugin:
    """

    """

    @abstract
    def extract_data(self, obj: Any) -> list[PlotData]:
        """

        Parameters
        ----------
        obj

        Returns
        -------

        """
        pass


    def update_style(self, data_index: int, **kwargs) -> dict:
        """

        Parameters
        ----------
        kwargs

        Returns
        -------

        """
        return kwargs