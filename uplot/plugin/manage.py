from uplot.plugin.IPlotPlugin import IPlotPlugin


REGISTERED_TYPES: dict[type, IPlotPlugin] = {}


def is_registered(t: type) -> bool:
    """
    Checks whether type **t** is registered and has a handler.
    """
    return t in REGISTERED_TYPES


def register(t: type, handler: IPlotPlugin, force: bool = False) -> bool:
    """
    Register a handler for the specified type **t**.

    Parameters
    ----------
    t : type
        The type to register.

    handler : IPlotPlugin
        The plugin for data extraction from the specified type **t**.

    force : bool, optional
        If True, set the handler even if a handler is already registered for the type.

    Returns
    -------
    bool
        True if registration is successful, False otherwise.
    """
    if is_registered(t) and not force:
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