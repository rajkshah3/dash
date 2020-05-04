#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np


df = pd.read_csv('dataset_combined.csv')
def make_dict(df,col='center'):
    unique_list = df[col].unique()
    df_out = dict()
    df = df.sort_values(by=['dteday'], ascending=True)
    idx = pd.date_range(df['dteday'].iloc[0], df['dteday'].iloc[-1], freq='H', name='dteday')
    for i in unique_list:
        ddf = df[df[col] == i]
        ddf['call_diff'] = abs(ddf['calls'] - ddf['answered'] - ddf['abandoned'])

        ddf['dteday'] = pd.to_datetime(ddf['dteday'])    
        ddf = ddf.set_index('dteday').reindex(idx).reset_index(drop=False)
        df_out[i] = ddf.set_index('dteday')
        # print(df_out[i].head(100))
    return df_out

month_dict={  1:'Jan',
            2:'Feb',
            3:'Mar',
            4:'Apr',
            5:'May',
            6:'Jun',
            7:'Jul',
            8:'Aug',
            9:'Sep',
            10:'Oct',
            11:'Nov',
            12:'Dec'
            }
df_dict = make_dict(df,'center')

times = {'Day':'D','Week':'W','Month':'M','Year':'Y'}



app = dash.Dash(__name__)

app.layout =    html.Div(style={'padding': 10},children=[

                    html.H1(children='Hello Dash'),
                    dcc.Dropdown(
                        id='time-dropdown',
                        options=[{'label': k, 'value': k} for k in times.keys()],
                        value='Month'
                        ),
                    dcc.Graph(id='output-graph')

                ])


@app.callback(
    dash.dependencies.Output('output-graph', 'figure'),
    [dash.dependencies.Input('time-dropdown', 'value')]
)
def update_graph(time_dropdown):

    #DO SOME DATA PROCESSING

    graph =  {'data': list(go.Scatter(
                        x=df_dict[i]['calls'].resample(times[time_dropdown]).mean(),
                        y=df_dict[i]['answered'].resample(times[time_dropdown]).mean(),
                        text=df_dict[i]['calls'].resample(times[time_dropdown]).mean().index,
                        # x=df[df['continent'] == i]['gdp per capita'],
                        # y=df[df['continent'] == i]['life expectancy'],
                        # text=df[df['continent'] == i]['country'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in df_dict.keys() 
                ),
            'layout': go.Layout(
                        title='Average answered vs total over {}'.format(time_dropdown),
                        xaxis={'title': 'Total Calls'},
                        yaxis={'title': ' Answered Calls'},
                        # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )
        }
    return graph

if __name__ == '__main__':
    app.run_server(debug=True)
