from typing import Literal
from uplot.utool import StrEnum


class Interpolator(StrEnum):
    NEAREST = 'nearest'
    LINEAR = 'linear'
    CUBIC = 'cubic'


class AspectMode(StrEnum):
    AUTO = 'auto'
    EQUAL = 'equal'


LineStyle = Literal[
     '-', # solid line
    '--', # dashed line
     ':', # dotted line
    '-.', # dash-dot line
     ' ', # no line
]

MarkerStyle = Literal[
    '.', # point
    ',', # pixel
    'o', # circle
    'v', # triangle down
    '^', # triangle up
    '<', # triangle left
    '>', # triangle right
    '1', # tri down
    '2', # tri up
    '3', # tri left
    '4', # tri right
    '8', # octagon
    's', # square
    'p', # pentagon
    '*', # star
    'h', # hexagon1
    'H', # hexagon2
    '+', # plus
    'x', # x
    'X', # x filled
    'D', # diamond
    'd', # thin diamond
    '|', # vline
    '_', # hline
    'P', # plus filled
]

"""
Common colormaps:
- plotly: https://plotly.com/python/builtin-colorscales/
- matplotlib: https://matplotlib.org/stable/users/explain/colors/colormaps.html  
"""
Colormap = Literal[
    'magma',
    'inferno',
    'plasma',
    'viridis',
    'cividis',
    'twilight',
    'turbo',
    'Blues',
    'BrBG',
    'BuGn',
    'BuPu',
    'GnBu',
    'Greens',
    'Greys',
    'OrRd',
    'Oranges',
    'PRGn',
    'PiYG',
    'PuBu',
    'PuBuGn',
    'PuOr',
    'PuRd',
    'Purples',
    'RdBu',
    'RdGy',
    'RdPu',
    'RdYlBu',
    'RdYlGn',
    'Reds',
    'Spectral',
    'YlGn',
    'YlGnBu',
    'YlOrBr',
    'YlOrRd',
    'gray',
    'hot',
    'hsv',
    'jet',
    'ocean',
    'rainbow',
]