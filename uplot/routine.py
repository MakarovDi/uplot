from numpy import ndarray
from typing import Sequence
from typing import TypeVar


# generic type
T = TypeVar('T')

def unpack_param(param: T | list[T] | None, idx: int) -> T | None:
    # default
    if param is None:
        return None

    # one param specified
    if isinstance(param, str):
        return param

    # multiple parameters, return one by index
    assert isinstance(param, Sequence)
    if idx < len(param):
        return param[idx]

    # few items parametrized but not all
    return None