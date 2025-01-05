from uplot.info import __version__, __author__, __email__  # noqa: F401

# engine managing
import uplot.engine as engine

# interface
from uplot.interface import IFigure, IPlotEngine

# main API function
from uplot.plot import figure

# common routines
import uplot.color as color

# common types
from uplot.utype import LineStyle, MarkerStyle, AspectMode, Colormap

# settings
from uplot.default import DEFAULT


__all__ = [
    
    # modules

    'engine',
    'color',

    # interface

    'IFigure', 
    'IPlotEngine',
    
    # functions
    
    'figure',

    # types
   
    'LineStyle', 
    'MarkerStyle', 
    'AspectMode', 
    'Colormap',

    # variables / constants

    'DEFAULT'
]