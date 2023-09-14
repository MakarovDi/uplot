from uplot.interface import IPlotEngine


DEFAULT_ENGINES: dict[str, IPlotEngine] = { }
DEFAULT_ENGINES_SHORT_NAME: dict[str, str] = { }


def available(short_names: bool = False) -> tuple[str, ...]:
    if short_names:
        return tuple(DEFAULT_ENGINES_SHORT_NAME.keys())
    else:
        return tuple(DEFAULT_ENGINES.keys())


def register(e: IPlotEngine, name: str, short_name: str = '') -> bool:
    assert name not in DEFAULT_ENGINES, 'the engine name must be unique'
    assert short_name not in DEFAULT_ENGINES_SHORT_NAME, 'the engine short name must be unique'

    if not e.is_available():
        return False

    DEFAULT_ENGINES[name] = e

    if short_name != '':
        DEFAULT_ENGINES_SHORT_NAME[short_name] = name

    return True