from uplot.interface import IPlotEngine, IFigure


class PlotlyEngine5(IPlotEngine):
    PLOT_WIDTH = 1000
    PLOT_HEIGHT = 800
    FILE_RESOLUTION_SCALE = 2
    MARKER_SIZE = 8
    LINE_WIDTH = 2
    RANGE_EXTRA_SPACE_PERCENT = 2 # adding extra space to min/max ranges

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


    def __init__(self):
        import plotly.graph_objs as go
        import plotly.io as pio
        self._pio = pio
        self._go = go
        # load style
        from uplot.engine.style.plotly import bmh
        self._layout_style = bmh

    def figure(self) -> IFigure:
        from uplot.engine.PlotlyFigure5 import PlotlyFigure5

        fig = PlotlyFigure5(self)

        # adjust style layout
        fig.internal.update_layout(template=self._layout_style,
                                   width=self.PLOT_WIDTH,
                                   height=self.PLOT_HEIGHT)

        return fig