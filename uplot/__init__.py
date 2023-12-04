from uplot.info import __version__, __author__, __email__

# engine managing
import uplot.engine as engine

# interface
from uplot.interface import IFigure, IPlotEngine

# main API function
from uplot.plot import figure

# common routines
import uplot.color as color

# common types
from uplot.LineStyle import LineStyle
from uplot.MarkerStyle import MarkerStyle
from uplot.AspectMode import AspectMode
from uplot.Colormap import Colormap

# settings
from uplot.default import DEFAULT