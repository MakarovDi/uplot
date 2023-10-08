from typing import Sequence
from typing import TypeVar


# generic type
T = TypeVar('T')

def unpack_param(param: T | list[T] | None, idx: int) -> T | None:
    """
    Get param by index:
        * param is None -> None
        * param is T -> param
        * param is list[T] -> param[idx]
        * param is list[T] -> None if out of range
    """
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

def kwargs_extract(kw: dict, name: str, default):
    """
    Get and delete parameter "name" from kw dict.
    """
    value = kw.get(name)

    if value is not None:
        del kw[name]
    else:
        value = default

    return value