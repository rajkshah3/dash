#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np


x_coord = np.arange(0,4*np.pi,4*np.pi/40)
sf_data = np.sin(x_coord)
ml_data = np.sin(x_coord+ 0.1)
ld_data = np.sin(2*x_coord + 0.4)

graph = dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': x_coord, 'y': sf_data, 'text' : sf_data, 'type': 'line', 'name': 'SF'},
                    {'x': x_coord, 'y': ml_data, 'type': 'line', 'name': u'Montréal'},
                    {'x': x_coord, 'y': ld_data, 'type': 'line', 'name': u'London'},

                ]
            }
        )

app = dash.Dash(__name__)

app.layout =    html.Div(style={'padding': 10},children=[

                    html.H1(children='Hello Dash'), 
                    graph

                ])


if __name__ == '__main__':
    app.run_server(debug=True)
