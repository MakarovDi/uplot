from uplot.interface import IPlotEngine, IFigure


class MatplotEngine(IPlotEngine):
    AUTOMATIC_MPL_BACKEND: str | None = None # automatically chosen matplotlib backend

    NON_GUI_BACKEND: set = {
         'agg',    # standard built-in
         'ipympl', # jupyter
        r'module://matplotlib_inline.backend_inline' # jupyter
    }

    @classmethod
    def is_available(cls) -> bool:
        try:
            import matplotlib
            return True
        except ImportError:
            return False

    @property
    def figure_type(self) -> type:
        return self.plt.Figure

    @property
    def plt(self):
        return self._plt

    @property
    def mpl(self):
        return self._mpl

    @property
    def is_gui_backend(self) -> bool:
        return not self.mpl.get_backend() in self.NON_GUI_BACKEND


    # noinspection PyPackageRequirements
    def __init__(self, backend: str | None = None):
        import matplotlib as mpl
        from matplotlib import pyplot as plt

        self._mpl = mpl
        self._plt = plt

        if self.AUTOMATIC_MPL_BACKEND is None:
            # save default matplotlib backend for future use
            self.AUTOMATIC_MPL_BACKEND = mpl.get_backend()

        if backend is None:
            backend = self.AUTOMATIC_MPL_BACKEND

        self._backend = backend

    def init(self):
        self._mpl.use(backend=self._backend)
        self.plt.style.use('bmh')

    def figure(self) -> IFigure:
        from uplot.engine.MatplotFigure import MatplotFigure
        self.init()
        return MatplotFigure(self)