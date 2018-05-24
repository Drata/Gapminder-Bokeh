from bokeh.plotting import ColumnDataSource, figure
from bokeh.models import HoverTool
from bokeh.models.annotations import Title
from bokeh.io import show
import numpy as np
import pandas as pd

#Cargamos el dataset en un dataframe
df = pd.read_csv('gapminder_data.csv')

#Indexamos por año
df_year = df.set_index('Year')
gapminder = ColumnDataSource(df_year.loc[1970])

#Creamos la herramienta hover
hover = HoverTool(tooltips=[
    ("Region", "@region"),
])

#Creamos el grafico
p = figure(plot_width=600, plot_height=400, tools=[hover])
p.circle('fertility', 'life', color = "navy", alpha=0.5, source = gapminder)
t = Title()
t.text = '1970'
p.title = t
p.xaxis.axis_label = 'Fertility (children per woman)'
p.yaxis.axis_label = 'Life expectancy (years)'

show(p)

