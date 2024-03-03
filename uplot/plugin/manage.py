from uplot.plugin.IPlotPlugin import IPlotPlugin


REGISTERED_TYPES: dict[type, IPlotPlugin] = {}


def is_registered(t: type) -> bool:
    """
    Checks whether type **t** is registered and has a handler.
    """
    return t in REGISTERED_TYPES


def register(t: type, handler: IPlotPlugin) -> bool:
    """
    Registers handler for the specified type **t**.
    """
    if t in REGISTERED_TYPES:
        # already registered
        return False

    REGISTERED_TYPES[t] = handler
    return True


def get_handler(t: type) -> IPlotPlugin | None:
    """
    Get plotting plugin(handler) for the registered type.
    """
    if is_registered(t):
        return REGISTERED_TYPES[t]
    return None