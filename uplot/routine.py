from numpy import ndarray


def unpack_param(param: str | ndarray | list, idx: int):
    # default
    if param is None:
        return None

    # one param specified
    if isinstance(param, str):
        return param

    # multiple parameters, return one by index
    if idx < len(param):
        return param[idx]

    # few items parametrized but not all
    return None