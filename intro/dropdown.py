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

def concat_bool_list(size,sets,s):
    l = list(np.full(size, False, dtype=bool))
    n_in_grp = int(size/sets)
    # print(n_in_grp)
    for i in range(0,sets):
        l[s + i*n_in_grp] = True
    return l

df_dict = make_dict(df,'center')

times = {'Day':'D','Week':'W','Month':'M','Year':'Y'}

button_name = ['center1','center2','center3','center4','center5','center6','center7','center8','center9']

buttons = list([dict(label=button_name[i],method = 'update', args = [{'visible': concat_bool_list(18,2,i)}]) for i in range(0,9)])

print(buttons)

updatemenus = list([
                    dict(active=-1,
                        buttons=buttons
                        )
                ])

calls = [
            go.Line(
                    x=df_dict[i]['calls'].resample('d').mean().index,
                    y=df_dict[i]['calls'].resample('d').mean(),
                    mode='markers',
                    opacity=0.5,
                    marker={
                        'size': 10,
                        'symbol': 'star',
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                name=i
            ) for i in df_dict.keys() ]


calls_avg = [ go.Line(
                    x=df_dict[i]['calls'].resample('M').mean().index,
                    y=df_dict[i]['calls'].resample('M').mean(),
                name=i+'_mean'
            ) for i in df_dict.keys() ]

graph_data = calls + calls_avg

graph =     dcc.Graph(
                id='calls_and_average_dropdown',
                figure={
                    'data': graph_data,
                    'layout': go.Layout(
                        title='Average call difference per month',
                        xaxis={'title': 'Calls'},
                        yaxis={'title': 'Unaccounted calls'},
                        # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 1, 'y': 1},
                        hovermode='closest',
                        updatemenus=updatemenus
                    )
                }
            )

app = dash.Dash(__name__)

app.layout =    html.Div(style={'padding': 10},children=[

                    html.H1(children='Hello Dash'),
                    graph

                ])



if __name__ == '__main__':
    app.run_server(debug=True)
