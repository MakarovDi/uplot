from uplot.interface import IPlotEngine

# TODO: StrEnum


DEFAULT_ENGINES: dict[str, IPlotEngine] = {
    'matplot': ...,
    'matplot-silent': ..., # for saving plots only
    'plotly5': ...,
}


def available() -> list[str]:
    pass


def register(e: IPlotEngine, name: str):
    pass