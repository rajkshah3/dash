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


x_hm = list(df_dict['center_1']['calls'].resample('M').mean().index.map(lambda x: '{}/{}'.format(month_dict[x.month],x.year)))
y_hm = ['VDN {}'.format(i) for i in reversed(range(15))]

np.random.seed(12344321)

z_hm =np.random.uniform(0.5,2,size=(len(y_hm),len(x_hm)))
z_hm_arr = np.array(z_hm) #Copy array from list

def arg_condition(x):
    if(x<1):
        return 'Y'
    if(x<1.5):
        return 'M'
    else:
        return 'D'

def arg_condition_col(x):
    if(x<1):
        return 0
    if(x<1.5):
        return 1
    else:
        return 2

shp = z_hm_arr.shape #Save original shape
z_hm_text = np.reshape(z_hm,(-1)) #reshape to apply map
z_hm_col = np.array(list(map(arg_condition_col,z_hm_text))).reshape(shp) #apply map and reshape back
z_hm_text = np.array(list(map(arg_condition,z_hm_text))).reshape(shp) #apply map and reshape back


f_hm = ff.create_annotated_heatmap(z_hm_col, x=x_hm,y=y_hm,annotation_text=z_hm_text)

graph = dcc.Graph(
            id='heatmap',
            figure={
                'data': f_hm,
                'layout': go.Layout(
                    title='heatmap test',
                    xaxis={'title': 'xaxs'},
                    yaxis={'title': 'yaxis'},
                    hovermode='closest'
                )
            }
        )


print(f_hm)

app = dash.Dash(__name__)

app.layout =    html.Div(style={'padding': 10},children=[

                    html.H1(children='Hello Dash'), 
                    graph
                ])


if __name__ == '__main__':
    app.run_server(debug=True)
