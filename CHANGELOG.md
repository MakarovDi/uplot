# Changelog

## `[v0.2.0]` - ??.10.2023

#### Added
* `[interface]` engine-specific parameters via `kwargs`: `plot()`, `scatter()`, `legend()`.

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