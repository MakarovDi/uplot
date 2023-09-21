from uplot.interface import IFigure, IPlotEngine
from uplot import engine as e


CURRENT_ENGINE: IPlotEngine | None = None


def figure(engine: str | IPlotEngine | None = None,
           aspect_ratio: float = 0.8) -> IFigure:
    """
    Creates figure via specified or default engine.

    Parameters
    ----------
    engine :
        plotting engine object or name, if None then return previous or default engine

    Returns
    -------
    IFigure
        figure object
    """
    global CURRENT_ENGINE

    if engine is None:
        engine = CURRENT_ENGINE

    if isinstance(engine, IPlotEngine):
        return engine.figure(aspect_ratio=aspect_ratio)

    CURRENT_ENGINE = e.get(engine)
    return CURRENT_ENGINE.figure(aspect_ratio=aspect_ratio)