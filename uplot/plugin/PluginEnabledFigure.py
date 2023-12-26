from numpy.typing import ArrayLike
from typing import Any

from uplot import LineStyle, MarkerStyle
from uplot.interface import IFigure
import uplot.plugin as plugin


class PluginEnabledFigure(IFigure):
    """
    Intermediate plugin system layer.
    """

    def _plugin_plot(self, x           : ArrayLike | Any,
                           y           : ArrayLike | None = None,
                           z           : ArrayLike | None = None,
                           name        : str | None = None,
                           color       : str | None = None,
                           line_style  : LineStyle | None = None,
                           marker_style: MarkerStyle | None = None,
                           marker_size : int | None = None,
                           opacity     : float = 1.0,
                           legend_group: str | None = None,
                           **kwargs) -> bool:
        """
        Returns True is x is recognized as a custom type with associated plugin.
        In this case, the data will be automatically extracted from the object and visualized,
        no need for further actions. Otherwise, False and x, y, z are regular arrays.
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
            name = name if data.name is None else data.name
            params = handler.update_style(data_index=i,
                                          name=name,
                                          color=color,
                                          line_style=line_style,
                                          marker_style=marker_style,
                                          marker_size=marker_size,
                                          opacity=opacity,
                                          legend_group=legend_group,
                                          **kwargs)
            self.plot(x=data.x, y=data.y, z=data.z, **params)

        return True