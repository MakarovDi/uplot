import numpy as np

import uplot
import imageio.v3 as iio

## Run Mode

save_to_file = False
engine = 'mpl'

## Data

d1 = [4, 5, 6]

d2 = np.array([[1, 2, 3],
               [3, 2, 1]]).T

## Fig 1

f1 = uplot.figure(engine=engine)
f1.plot(d1, d2)
f1.scatter(3, 5, name='The lonely dot')
f1.title('Test')
f1.legend(True)
f1.sync_axis_scale()
f1.xlabel('X value')
f1.ylabel('Y value')

if save_to_file:
    f1.save('fig1.save.jpg')
    iio.imwrite('fig1.as_image.png', f1.as_image())
else:
    f1.show()

## Fig 2

f2 = uplot.figure(aspect_ratio=0.4)
f2.plot(d2.T)
f2.title('Test')
f2.legend(True)
f2.xlabel('X value')
f2.ylabel('Y value')
f2.xlim(-0.5)
f2.ylim(0)

if save_to_file:
    f2.save('fig2.save.jpg')
    iio.imwrite('fig2.as_image.png', f2.as_image())
else:
    f2.show(True)