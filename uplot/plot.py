from uplot.interface import IFigure, IPlotEngine
from uplot import engine as e


CURRENT_ENGINE: IPlotEngine | None = None


def figure(engine: str | IPlotEngine | None = None) -> IFigure:
    if isinstance(engine, IPlotEngine):
        return engine.new_figure()

    engine = e.get(engine)
    return engine.new_figure()