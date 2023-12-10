# TODO

## Next Release

- [x] Fixed size of the legend items for **matplotlib**
- [ ] **API**: `fig.legend_group(...)` or parameter `legend_group`
- [x] **README** refactoring
- [ ] API documentation

## Backlog

- [ ] **API**: return **IFigure** from all functions to allow chaining.
- [ ] **API**: plugin system for plotting of a custom object: `fig.visualize(obj)`
- [ ] `README` API description: supported functions per engine
- [ ] `README` Add name, description and shortcuts for all engines
- [ ] **API**: `opacity: float` -> `opacity: float | list[float]`
- [ ] **API**: `fig.bar(...)` 
- [ ] **API**: `fig.click_event(...)`
- [ ] **API**: `fig.hover_text(...)` 
- [ ] **API**: `fig.legend`: param for the legend location
- [ ] Unified styling
  - [x] Engine independent config: `uplot.DEFAULT`
- [ ] TeX support
- [ ] `DataFrame` support
- [ ] `Bokeh` engine

## Done

- [x] **API**: `fig.surface3d(...)`
- [x] Gallery
- [x] Changelog
- [x] **API**: `kwargs` to directly access underlying engine
- [x] **API**: aspect ratio param: `uplot.figure(..., aspect_ratio: float)`
- [x] **API**: `fig.plot3d(...)` and `fig.scatter3d(...)`