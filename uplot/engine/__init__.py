from uplot.engine.MatplotEngine import MatplotEngine
from uplot.engine.manage import available, register


# init default engines

if MatplotEngine.is_available():
    register(MatplotEngine(),              name='matplot',      short_name='mpl')
    register(MatplotEngine(backend='agg'), name='matplot-file', short_name='mpl-file')