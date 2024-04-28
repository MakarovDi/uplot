# TODO

## Next Release

- [x] **API**: `fig.hline()` and `fig.vline()`


## Backlog

- [ ] **API**: `fig.legend`: param for the legend location
- [ ] `README` Add name, description and shortcuts for all engines
- [ ] **API**: `fig.bar(...)` 
- [ ] `README` API description: supported functions per engine
- [ ] `README` example for non-gui (file) plotting
- [ ] **API**: `opacity: float` -> `opacity: float | list[float]`
- [ ] **API**: `fig.click_event(...)`
- [ ] Unified styling
  - [x] Engine independent config: `uplot.DEFAULT`
- [ ] TeX support
- [ ] `DataFrame` support
- [ ] `Bokeh` engine

## Done

- [x] **API**: plugin system for plotting of a custom object
- [x] **API**: `fig.legend_group(...)` or parameter `legend_group`
- [x] **API**: return **IFigure** if possible to allow chaining
- [x] Fixed size of the legend items for **matplotlib**
- [x] **README** refactoring
- [x] API documentation
- [x] **API**: `fig.surface3d(...)`
- [x] Gallery
- [x] Changelog
- [x] **API**: `kwargs` to directly access underlying engine
- [x] **API**: aspect ratio param: `uplot.figure(..., aspect_ratio: float)`
- [x] **API**: `fig.plot3d(...)` and `fig.scatter3d(...)`