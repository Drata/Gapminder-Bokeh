from bokeh.plotting import ColumnDataSource, figure
from bokeh.models import HoverTool, CategoricalColorMapper, ColorBar, LogTicker, Slider, Select
from bokeh.models.annotations import Title
from bokeh.layouts import row, column, widgetbox
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
year = 1970
df_year = df.set_index('Year')
gapminder = ColumnDataSource(df_year.loc[year])

#Creamos la herramienta hover
hover = HoverTool(tooltips=[
    ("Country", "@Country"),
])

#Configuramos el color mapper
color_mapper = CategoricalColorMapper(factors = ['South Asia', 'Europe & Central Asia','Middle East & North Africa', 'Sub-Saharan Africa', 'America', 'East Asia & Pacific'], palette = brewer['Spectral'][6])

#Creamos el grafico
p = figure(plot_width=600, plot_height=400, tools=[hover], x_range=(x_min, x_max), y_range=(y_min, y_max))
p.circle('fertility', 'life', color = {'field':'region', 'transform':color_mapper}, alpha=1.0, legend='region', source = gapminder)
t = Title()
t.text = 'Gapminder Data for %d' % year
p.title = t
p.xaxis.axis_label = 'Fertility (children per woman)'
p.yaxis.axis_label = 'Life expectancy (years)'

#Añadimos el slider
slider = Slider(title='Year', 
	start=1970, end=2010, step=1, value=1970)
	
def callback_slider(attr, old, new):
	year = slider.value
	p.title.text = 'Gapminder Data for %d' % year
	new1 = ColumnDataSource(df_year.loc[year])
	gapminder.data = new1.data

slider.on_change('value', callback_slider)

#Añadimos los selectores
x_axis_menu = Select(options=['fertility','life'], value = 'fertility', title = "x-axis data")
y_axis_menu = Select(options=['fertility','life'], value = 'life', title = "y-axis data")

def callback_select_x(attr, old, new):
	p.circle(x_axis_menu.value, 'life', color = {'field':'region', 'transform':color_mapper}, alpha=1.0, legend='region', source = gapminder)
	if x_axis_menu.value == 'fertility': 
		p.xaxis.axis_label = 'Fertility (children per woman)'
	elif x_axis_menu.value == 'life': 
		p.xaxis.axis_label = 'Life expectancy (years)'
		
x_axis_menu.on_change('value', callback_select_x)

col = column(widgetbox(slider), widgetbox(x_axis_menu))
layout = row(col, p)

curdoc().add_root(layout)
curdoc().title = "Gapminder"
