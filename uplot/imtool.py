import numpy as np
import numbers
from numpy import ndarray


def estimate_range(image: ndarray) -> int:
    """
    Guess the range by an image type and values
    """
    # int image
    if image.dtype.type == np.uint8:
        return 255

    if image.dtype.type == np.uint16:
        return 65535

    # float image
    max_value = np.max(image)

    if max_value < 1.05:
        return 1.0

    if max_value < 255:
        return 255

    if max_value < 65535:
        return 65535

    raise RuntimeError('image range detection failure')