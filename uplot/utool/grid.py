import numpy as np
from uplot.utool import StrEnum


class Interpolator(StrEnum):
    NEAREST = 'nearest'
    LINEAR = 'linear'
    CUBIC = 'cubic'


def array_to_grid(x: np.ndarray,
                  y: np.ndarray,
                  z: np.ndarray,
                  interpolation: Interpolator,
                  interpolation_range: int) -> (np.ndarray, np.ndarray, np.ndarray):
    """
    Convert array of points (non-uniform grid) to uniform grid via interpolation.

    Parameters
    ----------
    x, y:
        1D array of coordinate.
    z:
        1D array of corresponding value for (x, y).

    Returns
    -------
    (np.ndarray, np.ndarray, np.ndarray)
        x, y, z - 2D arrays of uniform grid coordinates and 2D array of corresponding values.
    """
    assert len(x) == len(y) == len(z), 'sizes of x, y, z must match'
    from scipy.interpolate import griddata

    #
    x_range = np.linspace(x.min(), x.max(), num=interpolation_range)
    y_range = np.linspace(y.min(), y.max(), num=interpolation_range)

    z = griddata((x, y), z, (x_range[None, :], y_range[:, None]),
                 method=interpolation)
    x, y = np.meshgrid(x_range, y_range)

    return x, y, z