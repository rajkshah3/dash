#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('dataset_combined.csv')
print(df.head())

#        'legendgroup': 'group2'  group items in legend
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

calls = [
            go.Line(
                    x=df_dict[i]['calls'].resample('d').mean().index,
                    y=df_dict[i]['calls'].resample('d').mean(),
                    mode='markers',
                    opacity=0.5,
                    marker={
                        'size': 10,
                        'symbol': 'line_ns',
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                name=i
            ) for i in df_dict.keys() ]


calls_avg = [ go.Line(
                    x=df_dict[i]['calls'].resample('M').mean().index,
                    y=df_dict[i]['calls'].resample('M').mean(),
                name=i+'_mean'
            ) for i in df_dict.keys() ]

calls_avg_stdup = [ go.Line(
                    x=df_dict[i]['calls'].resample('M').mean().index,
                    y=pd.Series(df_dict[i]['calls'].resample('M').mean()).add(df_dict[i]['calls'].resample('d').mean().resample('M').std()),
                    name=i+'_stdup',
                    line=dict(dash='dot')
            ) for i in df_dict.keys() ]

calls_avg_stddwn = [ go.Line(
                    x=df_dict[i]['calls'].resample('M').mean().index,
                    y=pd.Series(df_dict[i]['calls'].resample('M').mean() - df_dict[i]['calls'].resample('d').mean().resample('M').std()),
                    name=i+'_stddwn',
                    line=dict(dash='dot')

            ) for i in df_dict.keys() ]


calls_p_avg = calls + calls_avg

calls_p_avg_up_dwn = calls + calls_avg + calls_avg_stdup + calls_avg_stddwn

updatemenus = list([
    dict(active=-1,
        buttons=list([
            dict(label = 'center_1',
                method = 'update',
                args = [{'visible': concat_bool_list(18,2,0)},
                        {'title': 'center_1' }
                    ],
                ),
            dict(label = 'center_2',
                method = 'update',
                args = [{'visible': concat_bool_list(18,2,1)},
                        {'title': 'center_2' }
                    ]
                ),
            dict(label = 'center_3',
                method = 'update',
                args = [{'visible': concat_bool_list(18,2,2)},
                        {'title': 'center_3' }
                    ]
                )                
            ])
        )
    ])

name = ['center1','center2','center3','center4','center5','center6','center7','center8','center9']

buttons = list([dict(label=name[i],method = 'update', args = [{'visible': concat_bool_list(18,2,i)}]) for i in range(0,9)])

buttons2 = list([dict(label=name[i],method = 'update', args = [{'visible': concat_bool_list(36,4,i)}]) for i in range(0,9)])


updatemenus2 = list([
    dict(active=-1,
        buttons=buttons
        )
    ])

updatemenus3 = list([
    dict(active=-1,
        buttons=buttons2
        )
    ])

df['dteday'] = pd.to_datetime(df['dteday'])
df = df.set_index('dteday')

# x_hm=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
x_hm = list(df_dict['center_1']['calls'].resample('M').mean().index.map(lambda x: '{}/{}'.format(month_dict[x.month],x.year)))
y_hm = ['VDN {}'.format(i) for i in reversed(range(50))]
# print(x_hm)
# x_hm=['Monday','Tuesday','Wednesday']
# y_hm=['Week 1','Week 2']

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

# _min = 0.5
# _max = 3
# color_scale= [[i,'rgb(0, 0, {})'.format(int(200*i/10))] for i in np.arange(_min, _max, (_max-_min)/10)]
color_scale= [[i,'rgb(0, 0, {})'.format(int(200*i/1))] for i in np.arange(0, 1, 0.1)]

f_hm = ff.create_annotated_heatmap(z_hm, x=x_hm,y=y_hm,annotation_text=z_hm_text,colorscale=color_scale)
f_hm2 = ff.create_annotated_heatmap(z_hm_col, x=x_hm,y=y_hm,colorscale='Blues',annotation_text=z_hm_text, hoverinfo='x+y+text', text = z_hm)
f_hm['layout']['margin']['l'] = 200
f_hm['layout']['yaxis']['tickfont']['size'] = 10

f_hm = [go.Heatmap(z=z_hm,x=x_hm,y=y_hm)]

times = {'Day':'D','Week':'W','Month':'M','Year':'Y'}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'padding': 10},children=[
    html.H1(children='Hello Dash'), 


    html.H2(children='''
        Sample tutorial dash graphs.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                {'x': [1, 2, 3], 'y': [1.5, 3, 6.4], 'type': 'bar', 'name': u'London'},

            ],
            'layout': {
                'title': 'Dash Data Visualizafftion'
            }
        }
    ),

    dcc.Graph(
        id='example-graph2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                {'x': [1, 2, 3], 'y': [1.5, 3, 6.4], 'type': 'bar', 'name': u'London'},

            ],
            'layout': {
                'title': 'Dash Data'
            }
        }
    ),

    html.H2(children='''
        Call center fake data graphs. 
    '''),

    html.Div(children='Generated by applying gaussian smearing to UCI bike rental dataset. (Bike rentals per hour)'),

    dcc.Graph(
        id='average-calls-month',
        figure={
            'data': [
                go.Scatter(
                    x=df_dict[i]['answered'].resample('M').mean(),
                    y=df_dict[i]['abandoned'].resample('M').mean(),
                    text=df_dict[i].resample('M').mean().index,
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
            ],
            'layout': go.Layout(
                title='Average answered vs abaondoned over month',
                xaxis={'title': 'Answered Calls'},
                yaxis={'title': 'Abandoned Calls'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),

    dcc.Graph(
        id='average-calls-daysoftheweek',
        figure={
            'data': [
                go.Scatter(
                    x=df_dict[i]['answered'].groupby(df_dict[i].index.dayofweek).mean(),
                    y=df_dict[i]['abandoned'].groupby(df_dict[i].index.dayofweek).mean(),
                    text=pd.Series(df_dict[i]['answered'].groupby(df_dict[i].index.dayofweek).mean().index).map(day_dict),
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
            ],
            'layout': go.Layout(
                title='Average answered vs abaondoned per day of the week',
                xaxis={'title': 'Answered Calls'},
                yaxis={'title': 'Abandoned Calls'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 1, 'y': 1},
                hovermode='closest'
            )
        }
    ),


    dcc.Graph(
        id='average-calls-year',
        figure={
            'data': [
                go.Scatter(
                    x=df_dict[i]['answered'].resample('Y').mean(),
                    y=df_dict[i]['abandoned'].resample('Y').mean(),
                    text=df_dict[i].resample('Y').mean().index.year,
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
                title='Average answered vs abaondoned over year',
                xaxis={'title': 'Answered Calls'},
                yaxis={'title': 'Abandoned Calls'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 1, 'y': 1},
                hovermode='closest'
            )
        }
    ),

    dcc.Graph(
        id='call_diff',
        figure={
            'data': [
                go.Scatter(
                    x=df_dict[i][df_dict[i]['call_diff'] > 3*df_dict[i]['call_diff'].std()]['call_diff'].index,
                    y=df_dict[i][df_dict[i]['call_diff'] > 3*df_dict[i]['call_diff'].std()]['call_diff'],
                    text=df_dict[i][df_dict[i]['call_diff'] > 3*df_dict[i]['call_diff'].std()]['call_diff'].index,
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
            ],
            'layout': go.Layout(
                title='Absolute difference between Total calls and (Answered + Abandoned). Where difference > 3\u03C3',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Unaccounted calls'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 1, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    
    dcc.Graph(
        id='call_diff_threshold',
        figure={
            'data': [
                go.Scatter(
                    x=df_dict[i][df_dict[i]['call_diff'] > 50]['call_diff'].index,
                    y=df_dict[i][df_dict[i]['call_diff'] > 50]['call_diff'],
                    text=df_dict[i][df_dict[i]['call_diff'] > 50]['call_diff'].index,
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
            ],
            'layout': go.Layout(
                title='Absolute difference between Total calls and (Answered + Abandoned). Where difference > 50',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Unaccounted calls'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 1, 'y': 1},
                hovermode='closest'
            )
        }
    ),

    dcc.Graph(
        id='call_diff_monthly',
        figure={
            'data': [
                go.Scatter(
                    x=df_dict[i]['calls'].resample('M').mean().index,
                    y=df_dict[i]['call_diff'].resample('M').mean(),
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
            ],
            'layout': go.Layout(
                title='Average monthly absolute difference between Total calls and (Answered + Abandoned)',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Unaccounted calls'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 1, 'y': 1},
                hovermode='closest'
            )
        }
    ),

    dcc.Graph(
        id='mean_call_diff_pmonth',
        figure={
            'data': [
                go.Scatter(
                    x=df_dict[i]['calls'].resample('M').mean(),
                    y=df_dict[i]['call_diff'].resample('M').mean(),
                    text=df_dict[i]['call_diff'].resample('M').mean().index,
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
            ],
            'layout': go.Layout(
                title='Average call difference per month vs total calls',
                xaxis={'title': 'Calls'},
                yaxis={'title': 'Unaccounted calls'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 1, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    

    dcc.Graph(
        id='mean_call_diff_pmonth_no_outliers',
        figure={
            'data': [
                go.Scatter(
                    x=df_dict[i][df_dict[i]['call_diff'] < 3*df_dict[i]['call_diff'].std()]['calls'].resample('M').mean(),
                    y=df_dict[i][df_dict[i]['call_diff'] < 3*df_dict[i]['call_diff'].std()]['call_diff'].resample('M').mean(),
                    text=df_dict[i][df_dict[i]['call_diff'] < 3*df_dict[i]['call_diff'].std()]['call_diff'].resample('M').mean().index,

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
            ],
            'layout': go.Layout(
                title='Average call difference per month (outliers removed)',
                xaxis={'title': 'Calls'},
                yaxis={'title': 'Unaccounted calls'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 1, 'y': 1},
                hovermode='closest'
            )
        }
    ),

    # dcc.Graph(
    #     id='call_centers_each_day',
    #     figure={
    #         'data': [
    #             go.Scatter(
    #                 x=df_dict[i][df_dict[i]['calls'].isnull() == True].index,

    #                 # x=df['center'].groupby(df.index).unique().index,
    #                 # y=df['center'].groupby(df.index).unique(),
    #                 # x=df[df['continent'] == i]['gdp per capita'],
    #                 # y=df[df['continent'] == i]['life expectancy'],
    #                 # text=df[df['continent'] == i]['country'],
    #                 mode='markers',
    #                 opacity=0.7,
    #                 marker={
    #                     'size': 15,
    #                     'line': {'width': 0.5, 'color': 'white'}
    #                 },
    #             name=i
    #         ) for i in df_dict.keys()

    #         ],
    #         'layout': go.Layout(
    #             title='Average call difference per month (outliers removed)',
    #             xaxis={'title': 'Calls'},
    #             yaxis={'title': 'Unaccounted calls'},
    #            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
    #             legend={'x': 0, 'y': 1},
    #             hovermode='closest'
    #         )
    #     }
    # ),


    dcc.Graph(
        id='calls_and_average',
        figure={
            'data': calls_p_avg,

            'layout': go.Layout(
                title='Average call difference per month (outliers removed)',
                xaxis={'title': 'Calls'},
                yaxis={'title': 'Unaccounted calls'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 1, 'y': 1},
                hovermode='closest'
            )
        }
    ),

    dcc.Graph(
        id='calls_and_average_dropdown',
        figure={
            'data': calls_p_avg,
            'layout': go.Layout(
                title='Average call difference per month (outliers removed)',
                xaxis={'title': 'Calls'},
                yaxis={'title': 'Unaccounted calls'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 1, 'y': 1},
                hovermode='closest',
                updatemenus=updatemenus
            )
        }
    ),
    dcc.Graph(
        id='calls_and_average_dropdown2',
        figure={
            'data': calls_p_avg,
            'layout': go.Layout(
                title='Average call difference per month (outliers removed)',
                xaxis={'title': 'Calls'},
                yaxis={'title': 'Unaccounted calls'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 1, 'y': 1},
                hovermode='closest',
                updatemenus=updatemenus2
            )
        }
    ),
    dcc.Graph(
        id='calls_and_average_dropdown_up_dwn',
        figure={
            'data': calls_p_avg_up_dwn,
            'layout': go.Layout(
                title='Average call difference per month (outliers removed)',
                xaxis={'title': 'Calls'},
                yaxis={'title': 'Unaccounted calls'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 1, 'y': 1},
                hovermode='closest',
                updatemenus=updatemenus3
            )
        }
    ),
    dcc.Graph(
        id='heatmap',
        # style={
        #     'display':'inline-block',
        #     'maxHeight': 900,
        #     'maxWidth': 1400,
        #     'margin': 100,
        #     'textAlign': 'center'
        # },
        figure={
            'data': f_hm,
            # 'layout': go.Layout(
            # title='heatmap test',
            # xaxis={'title': 'xaxs'},
            # yaxis={'title': 'yaxis'},
            # hovermode='closest',
            # )
        }
    ),

    dcc.Graph(
        id='heatmap2',
        figure={
            'data': f_hm2,
            'layout': go.Layout(
            title='heatmap test',
            xaxis={'title': 'xaxs'},
            yaxis={'title': 'yaxis'},
            hovermode='closest'
            )
        }
    ),

    dcc.Graph(
        id='heatmap3',
        figure={
            'data': f_hm2,
            'layout': go.Layout(
            title='heatmap test',
            xaxis={'title': 'xaxs'},
            yaxis={'title': 'yaxis'},
            hovermode='closest'
            )
        }
    ),

    dcc.Graph(
        id='heatmap4',
        figure={
            'data': f_hm2,
            'layout': go.Layout(
            title='heatmap test',
            xaxis={'title': 'xaxs'},
            yaxis={'title': 'yaxis'},
            hovermode='closest'
            )
        }
    ),

    dcc.Graph(
        id='heatmap5',
        figure={
            'data': f_hm2,
            'layout': go.Layout(
            title='heatmap test',
            xaxis={'title': 'xaxs'},
            yaxis={'title': 'yaxis'},
            hovermode='closest'
            )
        }
    ),

    dcc.Dropdown(
        id='time-dropdown',
        options=[{'label': k, 'value': k} for k in times.keys()],
        value='Month'
        ),

    dcc.Graph(id='indicator-graphic'),

    dcc.Dropdown(
    id='time-dropdown-2',
    options=[{'label': k, 'value': k} for k in times.keys()],
    value='Month'
    ),

    dcc.Dropdown(
    id='col-dropdown-1',
    options=[{'label': k, 'value': k} for k in df_dict['center_1'].columns if np.issubdtype(df_dict['center_1'][k].dtype, np.number)], #if df_dict['center_1'][k].isnumeric
    value='calls'
    ),

    dcc.Dropdown(
    id='col-dropdown-2',
    options=[{'label': k, 'value': k} for k in df_dict['center_1'].columns if np.issubdtype(df_dict['center_1'][k].dtype, np.number)], #if df_dict['center_1'][k].isnumeric
    value='answered'
    ),

    dcc.Graph(id='indicator-graphic-2')



])


# https://dash.plot.ly/getting-started-part-2

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('time-dropdown', 'value')]
)

def update_graph(time_dropdown):
    return  {'data': list(go.Scatter(
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
                title='Average answered vs total over month',
                xaxis={'title': 'Total Calls'},
                yaxis={'title': ' Answered Calls'},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
                    )
        }


@app.callback(
    dash.dependencies.Output('indicator-graphic-2', 'figure'),
    [dash.dependencies.Input('time-dropdown-2', 'value'),
    dash.dependencies.Input('col-dropdown-1', 'value'),
    dash.dependencies.Input('col-dropdown-2', 'value'),
    ]
)

def update_graph(time_dropdown,col1,col2):

    return  {'data': list(go.Scatter(
                        x=df_dict[i][col1].resample(times[time_dropdown]).mean(),
                        y=df_dict[i][col2].resample(times[time_dropdown]).mean(),
                        text=df_dict[i][col1].resample(times[time_dropdown]).mean().index,
                        # x=df[df['continent'] == i]['gdp per capita'],
                        # y=df[df['continent'] == i]['life expectancy'],
                        # text=df[df['continent'] == i]['country'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'black'},
                            'symbol':'line-ns'
                        },
                        name=i
                    ) for i in df_dict.keys() 
                ),
                'layout': go.Layout(
                title='Average answered vs total over month',
                xaxis={'title': col1},
                yaxis={'title': col2},
                # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
                    )
        }

        
# @app.callback(
#     dash.dependencies.Output('time-dropdown', 'figure'),
#     [dash.dependencies.Input('year-slider', 'value')])
# def update_figure(selected_year):
#     filtered_df = df[df.year == selected_year]
#     traces = []
#     for i in filtered_df.continent.unique():
#         df_by_continent = filtered_df[filtered_df['continent'] == i]
#         traces.append(go.Scatter(
#             x=df_by_continent['gdpPercap'],
#             y=df_by_continent['lifeExp'],
#             text=df_by_continent['country'],
#             mode='markers',
#             opacity=0.7,
#             marker={
#                 'size': 15,
#                 'line': {'width': 0.5, 'color': 'white'}
#             },
#             name=i
#         ))

#     return {
#         'data': traces,
#         'layout': go.Layout(
#             xaxis={'type': 'log', 'title': 'GDP Per Capita'},
#             yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
#             margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#             legend={'x': 0, 'y': 1},
#             hovermode='closest'
#         )
#     }


##Marker symbols
symbols = ['circle', 'square', 'cross', 'star']


if __name__ == '__main__':
    app.run_server(debug=True)
