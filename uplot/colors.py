from typing import OrderedDict

default_colors = OrderedDict[str, str]([
    ('blue'   , '#1f77b4'),
    ('orange' , '#ff7f0e'),
    ('green'  , '#2ca02c'),
    ('red'    , '#d62728'),
    ('purple' , '#9467bd'),
    ('brown'  , '#8c564b'),
    ('magenta', '#e377c2'),
    ('gray'   , '#7f7f7f'),
    ('yellow' , '#bcbd22'),
    ('cyan'   , '#17becf'),
])


color_short_name = {
    'b': default_colors['blue'],
    'g': default_colors['gren'],
    'r': default_colors['red'],
    'c': default_colors['cyan'],
    'm': default_colors['magenta'],
    'y': default_colors['yellow'],
    'k': '#000000',
    'w': '#ffffff'
}