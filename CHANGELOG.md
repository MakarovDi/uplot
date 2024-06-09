# Changelog

## `[v0.6.1]` - 09.06.2024

#### Fixed
* `[engine]` fixed returning `IFigure` for `reset_color()`
* `[engine.plotly5]` signature for `surface3d` fixed

#### Changed
* `[engine]` added extra aliases for non-GUI Matplotlib: `mpl-io`, `mpl-file`
* `[plugin]` added `force` parameter for `register()` to allow plugin replacement
* `[plugin]` plugin can be registered for homogeneous arrays like `list[T]` or `tuple[T, ...]`


## `[v0.6.0]` - 28.04.2024

#### Added
* `[interface] & [engine]` functions `hline()`, `vline()`


## `[v0.5.0]` - 03.02.2024

#### Added
* `[plugin]` plugin system to support custom objects plotting

#### Changed
* `[interface]` API documentation improved


## `[v0.4.0]` - 21.12.2023

#### Added
* `[interface] & [engine]` parameter `legend_group` added

#### Changed
* `[interface]` return `IFigure` when possible to support chaining


## `[v0.3.1]` - 11.12.2023

#### Changed
* `[interface] & [engine]` marker size is fixed in the legend, by default
* `[interface]` API documentation

#### Fixed
* `[engine.matplot]` remove the empty legend space on `figure.legend(False)`


## `[v0.3.0]` - 06.12.2023

#### Added
* `[interface]` singleton `DEFAULT` for storing and controlling default parameters.
* `[interface]` 3d surface plotting: `figure.surface3d(...)`
* `[color]` class `ColorScroller` for maintaining automatic color switching for plotting.

#### Changed
* `[engine]` the engine management system reworked: `engine.get()`, `engine.available()`, `engine.register()`.

#### Fixed
* `[engine.plotly5]` legend item width increased to show dashed line correctly.
* `[engine.matplot]` problem with `figure.close()` fixed.


## `[v0.2.1]` - 13.11.2023

#### Fixed
* `[engine.plotly5]` fixed problem with `line_style` setting.


## `[v0.2.0]` - 12.11.2023

#### Added
* `[interface]` `[engine]` 3d plot & scatter.
* `[interface]` `[engine]` 3d plot support: `zlim()`, `zlabel()`.
* `[interface]` `[engine]` engine-specific parameters via `kwargs`: `plot()`, `scatter()`, `legend()`.
* `[engine]` "color per point" support for scatter.

#### Changed
* `[engine.matplot]` legend outside the plot (same as plotly legend).
* `[engine.matplot]` change from `tight_layout` to `constrained` for more predictable behavior.
* `[engine.matplot]` axis and frame disabled for `imshow()`.
* `[engine.plotly5]` fixed size of legend's markers.

#### Fixed
* `[engine.matplot]` problem with figure no-show / double-show in jupyter.
* `[engine.plotly5]` prevent name truncation (ellipsis) of a trace when hovering over.

## `[v0.1.0]` - 22.09.2023

Initial version