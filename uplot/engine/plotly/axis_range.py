import numpy as np
from typing import Literal


def estimate_axis_range(figure,
                        axis: Literal['x', 'y', 'z'],
                        mode: Literal['min', 'max']) -> float:
    """
    Setting only min or only max is not implemented in plotly,
    so manual estimation of min/max is required.

    https://github.com/plotly/plotly.js/issues/400
    https://github.com/plotly/plotly.py/issues/3634
    """
    if figure.data is None:
        raise RuntimeError('there is no any graph, use xlim/ylim after plotting or '
                           'specify both range_min and range_max')

    get_axis_data = {
        'x': lambda trace: trace.x,
        'y': lambda trace: trace.y,
        'z': lambda trace: trace.z,
    }[axis]

    minmax_estimate = {
        'min': np.min,
        'max': np.max,
    }[mode]

    minmax = []
    for trace_data in figure.data:
        values = get_axis_data(trace_data)
        minmax.append(minmax_estimate(values))

    return minmax_estimate(minmax)