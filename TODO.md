# TODO

## Next Release

- [ ] **API**: `fig.surface3d(...)`
- [ ] **API**: plugin system for plotting of a custom object: `fig.visualize(obj)`
- [ ] **API**: `fig.legend_group(...)` or parameter `legend_group`

## Backlog

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

- [x] Gallery
- [x] Changelog
- [x] **API**: `kwargs` to directly access underlying engine
- [x] **API**: aspect ratio param: `uplot.figure(..., aspect_ratio: float)`
- [x] **API**: `fig.plot3d(...)` and `fig.scatter3d(...)`