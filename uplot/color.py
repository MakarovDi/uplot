import numpy as np
from typing import OrderedDict

# TODO: ColorScroller class

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

default_colors_list = list(default_colors.keys())


color_short_name = {
    'b': default_colors['blue'],
    'g': default_colors['green'],
    'r': default_colors['red'],
    'c': default_colors['cyan'],
    'm': default_colors['magenta'],
    'y': default_colors['yellow'],
    'k': '#000000',
    'w': '#ffffff'
}

def decode_color(name: str | None):
    if name is None:
        return None

    if len(name) == 1:
        if name not in color_short_name:
            raise LookupError(f'{name} is not valid color name, use: {color_short_name.keys()}')
        return color_short_name[name]

    if name[0] == '#':
        return name

    if name not in default_colors:
        raise LookupError(f'{name} is not valid color name, use: {default_colors.keys()}')

    return default_colors[name]


def rgb_to_str(rgb: list | np.ndarray) -> str | list[str]:
    """
    Convert rgb value (or array of rgb values) to hex-string compatible with uplot API.

    Parameters
    ----------
    rgb:
        rgb value of [0, 1] range or array values (N x 3)

    Returns
    -------
    list[str]
        hex color string or array of strings
    """
    rgb = np.asarray(rgb)
    rgb = np.atleast_2d(rgb)
    assert rgb.shape[-1] == 3, 'input Nx3 array or list'
    assert rgb.max() <= 1.0, 'rgb value range must be [0, 1]'

    rgb255 = (rgb*255).astype(np.uint8)
    rgb_str = [ f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}' for rgb in rgb255 ]

    if len(rgb) == 1:
        return rgb_str[0] # single rgb value

    return rgb_str # rgb array