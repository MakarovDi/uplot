from uplot.engine.MatplotEngine import MatplotEngine
from uplot.engine.manage import available, register, get


# register available engines

if MatplotEngine.is_available():
    # the first registered engine is the default
    register(MatplotEngine(),              name='matplot',      short_name='mpl')
    register(MatplotEngine(backend='agg'), name='matplot-nogui', short_name='mpl-nogui')