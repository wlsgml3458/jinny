from bokeh.sampledata import us_states, us_counties, unemployment
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.io import show
from bokeh.layouts import row, widgetbox
from bokeh.models import Slider, ColumnDataSource,HoverTool,LogColorMapper,CDSView,BooleanFilter
from bokeh.palettes import Viridis6 as palette
from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.us_states import data as states
from bokeh.sampledata.unemployment import data as unemployment

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

us_states = us_states.data.copy()
us_counties = us_counties.data.copy()

del us_states["HI"]
del us_states["AK"]

state_xs = [us_states[code]["lons"] for code in us_states]
state_ys = [us_states[code]["lats"] for code in us_states]

county_xs=[us_counties[code]["lons"] for code in us_counties if us_counties[code]["state"] not in ["ak", "hi", "pr", "gu", "vi", "mp", "as"]]
county_ys=[us_counties[code]["lats"] for code in us_counties if us_counties[code]["state"] not in ["ak", "hi", "pr", "gu", "vi", "mp", "as"]]

county_colors = []
for county_id in us_counties:
    if us_counties[county_id]["state"] in ["ak", "hi", "pr", "gu", "vi", "mp", "as"]:
        continue
    try:
        rate = unemployment[county_id]
        idx = min(int(rate/2), 5)
    except KeyError:
        county_colors.append("black")

state_names =[state['name'] for state in states.values()]
color_mapper = LogColorMapper(palette=palette)


source = ColumnDataSource(data=dict(x=state_xs,
                                   y=state_ys,
                                   name=state_names
                                   ))

TOOLS ="pan,wheel_zoom,reset,hover,save"

"""year_slider = Slider(start = 2009, end=2017,value=1,step=1,title="Year")
show(widgetbox(year_slider))"""

output_file("choropleth.html", title="choropleth.py example")

p = figure(title="US Unemployment 2009", tools = TOOLS, toolbar_location="left",
    plot_width=1100, plot_height=700)

p.patches(county_xs, county_ys, fill_alpha=0.0,
    line_color="white", line_width=0.5)
p.patches('x', 'y', source=source, hover_color="blue",fill_alpha=0.0,
          line_color="black", line_width=2, line_alpha=0.3)

hover = p.select_one(HoverTool)
hover.point_policy ="follow_mouse"
hover.tooltips =[("Year", "@year"),("Name", "@name"),
                ("Unemployment rate","@unemployment%"),
                ("H1B visa","@rate")]

show(p)
