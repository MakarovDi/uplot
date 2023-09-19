from uplot.interface import IPlotEngine, IFigure


class PlotlyEngine5(IPlotEngine):

    @classmethod
    def is_available(cls) -> bool:
        try:
            import plotly
            return True
        except ImportError:
            return False

    @property
    def figure_type(self) -> type:
        return self.go.Figure

    @property
    def go(self):
        return self._go

    @property
    def pio(self):
        return self._pio


    # noinspection PyPackageRequirements
    def __init__(self):
        import plotly.graph_objs as go
        import plotly.io as pio
        self._pio = pio
        self._go = go

    def figure(self) -> IFigure:
        from uplot.engine.PlotlyFigure5 import PlotlyFigure5
        return PlotlyFigure5(self)