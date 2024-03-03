from abc import abstractmethod as abstract
from typing import Any, NamedTuple
from numpy.typing import ArrayLike

from uplot.utool import StrEnum
import uplot.plugin as plugin


class PlotData(NamedTuple):
    """
    Structure to hold plotting data.
    """
    x: ArrayLike
    y: ArrayLike
    z: ArrayLike | None = None
    name: str | None = None


class PlotType(StrEnum):
    """
    Enumeration of plot types.
    """
    PLOT = 'plot'
    SCATTER = 'scatter'
    SURFACE3D = 'surface3d'


class IPlotPlugin:
    """
    Plugin interface to support plotting of custom objects
    """

    @abstract
    def extract_data(self, obj: Any) -> list[PlotData]:
        """
        Extract plotting data (x,y,z) from the object.
        This function must be implemented for minimal object plotting support.
        To add more advanced support (style adjustment), implement `update_style` function.

        Parameters
        ----------
        obj:
            The object for data extraction.

        Returns
        -------
        list[PlotData]
            List of extracted data from the object.
        """
        pass


    def update_style(self, plot_type : PlotType,
                           data_index: int,
                           data_count: int,
                           data_name : str | None,
                           **kwargs) -> dict:
        """
        Fine-tunes plotting of the custom object.

        Parameters
        ----------
        plot_type:
            Plotting type.

        data_index:
            Index of the data in list[PlotData], see extract_data.

        data_count:
            Size of list[PlotData], see extract_data.

        data_name:
            Name of the data.

        kwargs:
            Current plotting style.
            Style parameters depend on plot_type.

        Returns
        -------
        dict
            Updated style (kwargs).
        """
        if data_name is not None:
            kwargs['name'] = data_name

        return kwargs


def plot(plot_method : callable,
         x           : ArrayLike | Any,
         y           : ArrayLike | None = None,
         z           : ArrayLike | None = None,
         **kwargs) -> bool:
    """
    Returns True if x is recognized as a custom type with an associated plugin.
    In this case, the data will be automatically extracted from the object and visualized.
    No further actions are needed.
    Otherwise, returns False, and x, y, z are regular arrays.
    """
    # check if x is a custom object or regular arrays
    x_type = type(x)
    if y is not None or z is not None or not plugin.is_registered(x_type):
        return False

    # get registered plugin for x
    handler = plugin.get_handler(x_type)
    # extract x,y,z from the object
    data_list = handler.extract_data(x)

    # plot all extracted data
    for i, data in enumerate(data_list):
        params = handler.update_style(plot_type=plot_method.__name__,
                                      data_index=i,
                                      data_count=len(data_list),
                                      data_name=data.name,
                                      **kwargs)
        plot_method(x=data.x, y=data.y, z=data.z, **params)

    return True