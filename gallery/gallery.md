# Gallery

1. [plot](#plot)  
   1.1. [2d](#2d)  
   1.2. [3d](#3d)  
1. [scatter](#scatter)  
   2.1. [2d](#2d)  
   2.2. [3d](#3d)  


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

![plot](asset/plot.png)

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

![plot-3d](asset/plot-3d.png)

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

![scatter](asset/scatter.png)


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

![scatter](asset/scatter-3d.png)