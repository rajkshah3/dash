#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np


x_coord = [1, 2, 3]
sf_data = [4, 1, 2]
ml_data = [2, 4, 5]
ld_data = [1.5, 3, 6.4]

app = dash.Dash(__name__)


graph =     dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': x_coord, 'y': sf_data, 'type': 'bar', 'name': 'SF'},
                {'x': x_coord, 'y': ml_data, 'type': 'bar', 'name': u'Montréal'},
                {'x': x_coord, 'y': ld_data, 'type': 'bar', 'name': u'London'},

            ]
        }
        )

app.layout = html.Div(style={'padding': 10},children=[dcc.Location(id='HelloSonia'),html.H1('Hello Sonia')])

graph = None

if __name__ == '__main__':
    app.run_server(debug=True)
