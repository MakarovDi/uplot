import numpy as np
from typing import Literal


def estimate_axis_range(figure,
                        axis: Literal['x', 'y', 'z'],
                        mode: Literal['min', 'max']) -> float:
    """
    Setting only min or only max is not implemented in plotly,
    so manual estimation of min/max is required:

        https://github.com/plotly/plotly.js/issues/400
        https://github.com/plotly/plotly.py/issues/3634
    """
    if figure.data is None:
        raise RuntimeError('there is no any graph, use xlim/ylim after plotting or '
                           'specify both range_min and range_max')

    # estimate min/max from data
    data_minmax = []
    for trace_data in figure.data:
        values = trace_data[axis]
        if np.issubdtype(values.dtype, np.number):
            # array of numbers
            minmax_estimate = { 'min': np.min, 'max': np.max }[mode]
        else:
            # array of str or other objects
            minmax_estimate = { 'min': lambda x: x[0], 'max': lambda x: x[-1] }[mode]

        data_minmax.append(minmax_estimate(values))

    minmax = minmax_estimate(data_minmax)

    # estimate min/max from range
    axis = {
        'x': 'xaxis',
        'y': 'yaxis'
    }[axis]

    axis_range = figure.layout[axis]['range']
    if axis_range is not None:
        minmax = minmax_estimate([ minmax, *axis_range ])

    return minmax