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

#Hover info
#https://dash.plot.ly/interactive-graphing
center_group={
    'center_1':'EUR',
    'center_2':'EUR',
    'center_3':'EUR',
    'center_4':'EUR',
    'center_5':'USA',
    'center_6':'USA',
    'center_7':'USA',
    'center_8':'ASIA',
    'center_9':'ASIA'
}

day_dict={  0:'Monday',
            1:'Tuesday',
            2:'Wednesday',
            3:'Thursday',
            4:'Friday',
            5:'Saturday',
            6:'Sunday'
            }

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

#Return a list of mainly falses, trues where periodically when datasets hav
#been concatenated
def concat_bool_list(size,sets,s):
    l = list(np.full(size, False, dtype=bool))
    n_in_grp = int(size/sets)
    # print(n_in_grp)
    for i in range(0,sets):
        l[s + i*n_in_grp] = True
    return l


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

df_dict = make_dict(df,'center')



graph =     dcc.Graph(
                id='average-calls-month',
                figure={
                    'data': [
                        go.Scatter(
                            x=df_dict[i]['answered'].resample('M').mean(),
                            y=df_dict[i]['abandoned'].resample('M').mean(),
                            text=df_dict[i].resample('M').mean().index,
                            mode='markers',
                            opacity=0.7,
                            marker={
                                'size': 15,
                                'line': {'width': 0.5, 'color': 'white'}
                            },
                            name=i
                        ) for i in df_dict.keys()
                    ],
                    'layout': go.Layout(
                        title='Average answered vs abaondoned over month',
                        xaxis={'title': 'Answered Calls'},
                        yaxis={'title': 'Abandoned Calls'},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
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
