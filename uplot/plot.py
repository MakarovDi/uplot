from uplot.interface import IFigure, IPlotEngine
from uplot import engine as e
from uplot.default import DEFAULT


CURRENT_ENGINE: IPlotEngine | None = None


def figure(engine      : str | IPlotEngine | None = None,
           width       : int | None = DEFAULT.figure_width,
           aspect_ratio: float = DEFAULT.figure_aspect_ratio) -> IFigure:
    """
    Create a new figure using the specified plotting engine or the default engine.

    Parameters
    ----------
    engine : str, IPlotEngine, or None, optional
        The plotting engine object, name, or None. If None, the function uses the previous or default engine.

    width : int or None, optional
        The width of the figure in pixels.

    aspect_ratio : float, optional
        The aspect ratio for the new figure.

    Returns
    -------
    IFigure
        The created figure object.

    Examples
    --------
    >>> fig = figure(engine='plotly', width=800, aspect_ratio=0.6)
    >>> fig.plot(x, y, name='Data')
    >>> fig.show()

    >>> fig = figure(width=1200)
    >>> fig.scatter(x, y)
    >>> fig.show()
    """
    global CURRENT_ENGINE

    if engine is None:
        engine = CURRENT_ENGINE

    if isinstance(engine, IPlotEngine):
        return engine.figure(width=width, aspect_ratio=aspect_ratio)

    CURRENT_ENGINE = e.get(engine)
    return CURRENT_ENGINE.figure(width=width, aspect_ratio=aspect_ratio)