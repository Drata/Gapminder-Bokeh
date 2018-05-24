from bokeh.plotting import ColumnDataSource, figure
from bokeh.models import HoverTool, CategoricalColorMapper, ColorBar, LogTicker
from bokeh.models.annotations import Title
from bokeh.io import show, curdoc
from bokeh.palettes import brewer
import numpy as np
import pandas as pd


#Cargamos el dataset en un dataframe
df = pd.read_csv('gapminder_data.csv')

#Obtenemos maximos y minimos para los ejes
y_min = min(df['life'])
y_max = max(df['life'])

x_min = min(df['fertility'])
x_max = max(df['fertility'])

#Indexamos por año
df_year = df.set_index('Year')
gapminder = ColumnDataSource(df_year.loc[1970])

#Creamos la herramienta hover
hover = HoverTool(tooltips=[
    ("Region", "@region"),
])

#Configuramos el color mapper
color_mapper = CategoricalColorMapper(factors = ['South Asia', 'Europe & Central Asia','Middle East & North Africa', 'Sub-Saharan Africa', 'America', 'East Asia & Pacific'], palette = brewer['Spectral'][6])

#Creamos el grafico
p = figure(plot_width=600, plot_height=400, tools=[hover], x_range=(x_min, x_max), y_range=(y_min, y_max))
p.circle('fertility', 'life', color = {'field':'region', 'transform':color_mapper}, alpha=1.0, legend='region', source = gapminder)
t = Title()
t.text = 'Gapminder Data for 1970'
p.title = t
p.xaxis.axis_label = 'Fertility (children per woman)'
p.yaxis.axis_label = 'Life expectancy (years)'

curdoc().add_root(p)
curdoc().title = "Gapminder"
