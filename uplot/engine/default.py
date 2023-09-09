from uplot.interface import IPlotEngine


DEFAULT_ENGINES: dict[str, IPlotEngine] = {
    'matplot': ...,
    'matplot-silent': ..., # for saving plots only
    'plotly5': ...,
}