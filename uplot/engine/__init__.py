from uplot.engine.MatplotEngine import MatplotEngine
from uplot.engine.PlotlyEngine5 import PlotlyEngine5
from uplot.engine.manage import available, register, get


# register available engines

if MatplotEngine.is_available():
    register(MatplotEngine(),              name='matplot',       short_name='mpl') # default
    register(MatplotEngine(backend='agg'), name='matplot-nogui', short_name='mpl-nogui')

if PlotlyEngine5.is_available():
    register(PlotlyEngine5(),              name='plotly5',       short_name='pl5')