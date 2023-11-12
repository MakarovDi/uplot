from uplot.interface import IFigure, IPlotEngine
from uplot import engine as e


CURRENT_ENGINE: IPlotEngine | None = None


def figure(engine: str | IPlotEngine | None = None,
           width : int | None = 800,
           aspect_ratio: float = 0.6) -> IFigure:
    """
    Creates figure via specified or default engine.

    Parameters
    ----------
    engine :
        plotting engine object or name, if None then return previous or default engine

    width :
        the figure width in pixels

    aspect_ratio :
        aspect ratio for the new figure

    Returns
    -------
    IFigure
        figure object
    """
    global CURRENT_ENGINE

    if engine is None:
        engine = CURRENT_ENGINE

    if isinstance(engine, IPlotEngine):
        return engine.figure(width=width, aspect_ratio=aspect_ratio)

    CURRENT_ENGINE = e.get(engine)
    return CURRENT_ENGINE.figure(width=width, aspect_ratio=aspect_ratio)