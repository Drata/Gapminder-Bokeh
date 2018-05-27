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

#Indexamos por año
df_year = df.set_index('Year')
gapminder = ColumnDataSource(df_year.loc[1970])

#Creamos la herramienta hover
hover = HoverTool(tooltips=[
    ("Country", "@Country"),
])

#Configuramos el color mapper
color_mapper = CategoricalColorMapper(factors = ['South Asia', 'Europe & Central Asia','Middle East & North Africa', 'Sub-Saharan Africa', 'America', 'East Asia & Pacific'], palette = brewer['Spectral'][6])

def create_figure():
	#Obtenemos maximos y minimos para los ejes
	y_min = min(df[y_axis_menu.value])
	y_max = max(df[y_axis_menu.value])
	
	x_min = min(df[x_axis_menu.value])
	x_max = max(df[x_axis_menu.value])
	
	p = figure(plot_width=600, plot_height=400, tools=[hover], x_range=(x_min, x_max), y_range=(y_min, y_max))
	p.circle(x_axis_menu.value, y_axis_menu.value, color = {'field':'region', 'transform':color_mapper}, alpha=1.0, legend='region', source = gapminder)
	t = Title()
	t.text = 'Gapminder Data for %d' % slider.value
	p.title = t
	p.xaxis.axis_label = x_axis_menu.value
	p.yaxis.axis_label = y_axis_menu.value
	
	return p

#Añadimos el slider
slider = Slider(title='Year', 
	start=1970, end=2010, step=1, value=1970)
	
def callback_slider(attr, old, new):
	layout.children[1].title.text = 'Gapminder Data for %d' % slider.value
	new1 = ColumnDataSource(df_year.loc[slider.value])
	gapminder.data = new1.data

slider.on_change('value', callback_slider)

#Añadimos los selectores
x_axis_menu = Select(options=['fertility', 'life', 'population', 'child_mortality'], value = 'fertility', title = "x-axis data")
y_axis_menu = Select(options=['fertility', 'life', 'population', 'child_mortality'], value = 'life', title = "y-axis data")

def callback_select_axis(attr, old, new):
	layout.children[1] = create_figure()
	
x_axis_menu.on_change('value', callback_select_axis)
y_axis_menu.on_change('value', callback_select_axis)

col = column(widgetbox(slider), widgetbox(x_axis_menu), widgetbox(y_axis_menu))
layout = row(col, create_figure())

curdoc().add_root(layout)
curdoc().title = "Gapminder"
