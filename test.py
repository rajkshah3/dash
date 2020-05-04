import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import datetime as dt
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('dataset_combined.csv')
print(df.head())




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
        print(df_out[i].head(100))
    return df_out

df_dict = make_dict(df,'center')



df['dteday'] = pd.to_datetime(df['dteday'])
df = df.set_index('dteday')


day_dict={  0:'Monday',
            1:'Tuesday',
            2:'Wednesday',
            3:'Thursday',
            4:'Friday',
            5:'Saturday',
            6:'Sunday'
            }

def get_day(i):
    if(i is 0):
        return 'Monday'

    return 'Tuesday'

# print(pd.Series(df_dict['center_1']['answered'].groupby(df_dict['center_1'].index.dayofweek).mean().index).map(day_dict))

# print(df_dict[i][df_dict[i]['call_diff'] < 3*df_dict[i]['call_diff'].std()]['call_diff'].resample('M').mean().index.month)

print(df['center'].groupby(df.index).unique())

z_hm=[
    [np.random.uniform(0.5,2),np.random.uniform(0.5,2),np.random.uniform(0.5,2)],
    [np.random.uniform(0.5,2),np.random.uniform(0.5,2),np.random.uniform(0.5,2)],
    [np.random.uniform(0.5,2),np.random.uniform(0.5,2),np.random.uniform(0.5,2)]
]

