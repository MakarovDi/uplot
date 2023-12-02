from uplot.interface import IFigure, IPlotEngine
from uplot import engine as e


CURRENT_ENGINE: IPlotEngine | None = None


def figure(engine: str | IPlotEngine | None = None,
           width : int | None = 800,
           aspect_ratio: float = 0.6) -> IFigure:
    """
    Creates a new figure using the specified plotting engine or the default engine.

    Parameters
    ----------
    engine : str, IPlotEngine, or None, optional
        The plotting engine object or name. If None, the function returns the previous or default engine.

    width : int or None, optional
        The width of the figure in pixels.

    aspect_ratio : float, optional
        The aspect ratio for the new figure.

    Returns
    -------
    IFigure
        The created figure object.
    """
    global CURRENT_ENGINE

    if engine is None:
        engine = CURRENT_ENGINE

    if isinstance(engine, IPlotEngine):
        return engine.figure(width=width, aspect_ratio=aspect_ratio)

    CURRENT_ENGINE = e.get(engine)
    return CURRENT_ENGINE.figure(width=width, aspect_ratio=aspect_ratio)