from uplot.interface import IPlotEngine, IFigure


class MatplotEngine(IPlotEngine):
    MARKER_SIZE = 6
    SHOWING_DPI = 100
    SAVING_DPI = SHOWING_DPI * 2

    AUTOMATIC_MPL_BACKEND: str | None = None # automatically chosen matplotlib backend

    NON_GUI_BACKEND: set = {
        r'agg', # standard built-in
        r'module://ipympl.backend_nbagg', # jupyter
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

    def figure(self, width: int, aspect_ratio: float) -> IFigure:
        from uplot.engine.MatplotFigure import MatplotFigure

        # use style and backend for our figure only
        # avoid to change global state of matplotlib
        current_backend = self._mpl.get_backend()
        self._mpl.use(backend=self._backend)

        # temporary styling:
        # https://matplotlib.org/stable/users/explain/customizing.html
        with self._plt.style.context('bmh'):
            fig = MatplotFigure(self)
            fig.internal.set_figwidth(width / self.SHOWING_DPI)
            fig.internal.set_figheight(aspect_ratio*(width / self.SHOWING_DPI))

        self._mpl.use(backend=current_backend)
        return fig