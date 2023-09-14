from uplot.interface import IPlotEngine, IFigure

class MatplotEngine(IPlotEngine):

    @classmethod
    def is_available(cls) -> bool:
        try:
            import matplotlib
            return True
        except ImportError:
            return False

    @property
    def fig_type(self) -> type:
        return self.plt.Figure

    @property
    def plt(self):
        return self._plt

    @property
    def mpl(self):
        return self._mpl


    # noinspection PyPackageRequirements
    def __init__(self, backend: str | None = None):
        import matplotlib as mpl
        from matplotlib import pyplot as plt

        self._mpl = mpl
        self._plt = plt
        self._backend = backend

    def init(self):
        if self._backend is not None:
            self._mpl.use(backend=self._backend)
        self.plt.style.use('bmh')

    def new_figure(self) -> IFigure:
        from uplot.engine.MatplotFigure import MatplotFigure
        self.init()
        return MatplotFigure(self)