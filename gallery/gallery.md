# Gallery

1. [plot](#plot)  
1. [scatter](#scatter)
1. [surface3d](#surface3d)  


> See also jupyter notebook: `gallery.ipynb`.

## plot

### 2d

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

<img src='asset/plot.png' width='700'>

### 3d

```python
import numpy as np
import uplot

x = np.linspace(0, np.pi*4, num=100)
y1 = np.sin(x)
y2 = np.sin(x - np.pi/4)

fig = uplot.figure(engine='plotly5')
fig.plot(x=y1, y=y2, z=x, name='data #1')
fig.plot(x=y1, y=y2, z=x+2, name='data #2')
fig.plot(x=y1, y=y2, z=x+4, name='data #1')
fig.legend()
fig.show()
```

<img src='asset/plot-3d.png' width='700'>

## scatter

### 2d

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

<img src='asset/scatter.png' width='700'>


### 3d

```python
import numpy as np
import uplot

z = np.linspace(0, np.pi*4, num=100)
x = np.sin(z)
y = np.sin(z - np.pi/4)

rgb_colors = np.random.uniform(low=0.1, high=0.9, size=[100, 3])

fig = uplot.figure(engine='plotly5')
fig.scatter(x, y, z, color=uplot.color.rgb_to_str(rgb_colors))
fig.show()
```

<img src='asset/scatter-3d.png' width='700'>

## surface3d

```python
x = np.arange(0, 5, 0.25)
y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig = uplot.figure('plotly', aspect_ratio=0.8)
fig.surface3d(x, y, Z,   name='data #1', colormap='blues')
fig.surface3d(x, y, Z*6, name='data #2', show_colormap=True)
fig.xlabel('X Axis')
fig.ylabel('Y Axis')
fig.zlabel('Z Axis')
fig.legend()
fig.show()
```

<img src='asset/surface3d.png' width='700'>