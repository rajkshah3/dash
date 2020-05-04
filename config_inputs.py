import pandas as pd
import numpy as np
from scipy.stats import truncnorm
from scipy.stats import logistic

df = pd.read_csv('bike_data.csv')

#Combine hours
df['dteday'] = pd.to_datetime(df['dteday'])
df['hr'] = pd.to_timedelta(df['hr'],unit='H')
df['dteday'] = df['dteday'] + df['hr']

print(df.head(30))

np.random.seed(12344321)
centers = {i:np.random.uniform(0.5,2) for i in list(range(1, 10)) }
sigmas = {i:np.random.uniform(0,8) for i in list(range(1, 10)) }

centers_avg_time = {i:np.random.uniform(8,15) for i in list(range(1, 10)) }

#abandoned = lambda x : truncnorm(0,1,loc=0.1, scale=0.3).rvs()

avg = df['cnt'].mean()
print(avg)

input_anomalae = lambda x : x*np.sqrt(x) if (np.random.uniform(0,5000) > 4995) else x 
input_small_anomalae = lambda x : int(np.random.uniform(0,20)) if (np.random.uniform(0,5000) > 4995) else x 
randomise = lambda x : int(abs(np.random.normal(x,x/2))) if (np.random.uniform(0,5000) > 4995) else x 
ldf = []

df = df.drop(['instant','season','yr','mnth','hr','holiday','weekday','workingday','atemp','hum','windspeed','casual','registered','temp','weathersit'],axis=1)

for i,j,k in zip(centers.keys(),sigmas.keys(),centers_avg_time.keys()):
	gaus = lambda x : round(abs(np.random.normal(centers[i]*x,sigmas[j])))
	df['calls_' + str(i)] = df['cnt'].apply(gaus)
	gaus2 = lambda x : round(abs(np.random.normal(x,0.8*sigmas[j])))
	df['calls_pred_' + str(i)] = df['calls_' + str(i)].apply(gaus2)
	
	abandoned = lambda x : round(x * abs(np.random.normal(0.1,0.3*1/(1+np.exp(-x/avg)))))
	df['abandoned_' + str(i)] = df['calls_' + str(i)].apply(abandoned)

	# _df1	 = df.loc[df['calls_' + str(i)] - df['abandoned_' + str(i)] > 0]
	# _df2	 = df.loc[df['calls_' + str(i)] - df['abandoned_' + str(i)] <= 0]

	# _df1['answered']  = _df1['calls_' + str(i)]  - _df1['abandoned_' + str(i)]
	# _df2['answered']  = 0
	# _df1['answered'].append(_df2['answered'])
	
	# df['answered_' + str(i)] = 0

	# df.loc[df['calls_' + str(i)] - df['abandoned_' + str(i),'answered_' + str(i)] = 

	df['answered_' + str(i)] = np.where(df['calls_' + str(i)]  - df['abandoned_' + str(i)] > 0, df['calls_' + str(i)]  - df['abandoned_' + str(i)] , 0)

	avg_time = lambda x : abs(np.random.normal(centers_avg_time[i],0.3*sigmas[j]))
	df['avg_time_' + str(i)] = df['answered_' + str(i)].apply(avg_time)
	df['time_' + str(i)] = df['avg_time_' + str(i)] * df['answered_' + str(i)]

	df['calls_' + str(i)] = df['calls_' + str(i)].apply(input_anomalae)
	df['calls_' + str(i)] = df['calls_' + str(i)].apply(input_small_anomalae)


	df['answered_' + str(i)] 	= df['answered_' + str(i)].apply(randomise)
	df['abandoned_' + str(i)] 	= df['abandoned_' + str(i)].apply(randomise)


	df_out = df[['dteday','calls_' + str(i),'time_' + str(i),'avg_time_' + str(i),'answered_' + str(i),'abandoned_' + str(i),'calls_pred_' + str(i)]]
	
	df_out = df_out.rename(index=str, columns={'calls_' + str(i): "calls", 'time_' + str(i): "time", 'avg_time_' + str(i): "avg_time", 'answered_' + str(i): "answered", 'abandoned_' + str(i): "abandoned", 'calls_pred_' + str(i): "calls_pred"})

	df_out['center'] = 'center_' + str(i)
	ldf.append(df_out)


output_df = pd.concat(ldf)

drop_indices = np.random.choice(output_df.index, int(len(output_df.index)/50), replace=False)
output_df = output_df.drop(drop_indices)

output_df.to_csv('dataset_combined.csv')

drop_indices = np.random.choice(df.index, int(len(df.index)/100), replace=False)
df = df.drop(drop_indices)

df.to_csv('dataset_split_row.csv')


print(df.head(30))

def print_anoms(df,col):
	print(col)
	df_out = df[df[col] > (df[col].mean() + 4* df[col].std())]
	print(len(df_out.index))
	print(df_out.head())

for i in df.columns:
	if(i[:4] == 'call'):
		print_anoms(df,i)
