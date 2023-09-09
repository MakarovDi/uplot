from uplot.interface import IFigure, IPlotEngine


CURRENT_ENGINE: IPlotEngine = None


def figure(engine: str | IPlotEngine | None = None) -> IFigure:
    pass