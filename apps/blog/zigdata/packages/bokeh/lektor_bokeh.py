# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
import os
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.resources import CDN
from bokeh.embed import file_html, json_item, components
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
import json

os.environ["BOKEH_LOG_LEVEL"] = "debug"

df = sea_surface_temperature.copy()
source = ColumnDataSource(data=df)

plot = figure(x_axis_type='datetime', y_range=(0, 25), y_axis_label='Temperature (Celsius)',
              width=500, height=500,
              title="Sea Surface Temperature at 43.18, -70.43")
plot.line('time', 'temperature', source=source)
script, div = components(plot)


class BokehPlugin(Plugin):
    name = 'bokeh'
    description = u'Bokeh plot renderer'

    def on_setup_env(self, **extra):
        self.env.jinja_env.globals.update(
            plotjs=script,
            plot_div=div
        )

    def on_process_template_context(self, context, **extra):
        def test_function():
            return 'Value from plugin %s' % self.name

        context['test_function'] = test_function
