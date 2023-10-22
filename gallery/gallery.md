# Gallery

1. [plot](#plot)
1. [scatter](#scatter)

> See `gallery.ipynb` for more examples.

## plot

```python
import numpy as np
import uplot

# data
x = np.linspace(0, np.pi*4, num=100)
y1 = np.sin(x)
y2 = np.sin(x + np.pi/4)
y3 = np.sin(x + 2*np.pi/4)
y4 = np.sin(x + 3*np.pi/4)

# plot
fig = uplot.figure(engine='plotly5')
fig.plot(x, y1, name='data #1')
fig.plot(x, y2, name='data #2')
fig.plot(x, y3, name='data #3')
fig.plot(x, y4, name='data #4')
fig.legend()
fig.show()
```

![plot](asset/plot.png)

## scatter

```python
import numpy as np
import uplot

# data
x = np.random.uniform(size=100)
y = np.random.uniform(size=100)
# random color per point
rgb_colors = np.random.uniform(low=0.3, high=0.8, size=[100, 3])

# plot
fig = uplot.figure(engine='plotly5')
fig.scatter(x, y)
fig.show()
```

![scatter](asset/scatter.png)