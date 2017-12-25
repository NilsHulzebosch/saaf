from get_polo_data import df_from_pickle
import torch

FILENAME = 'data_USDT_BTC_start_2014-01-01 01:00:00_period_300_retrieved_2017-12-25 16:51:38.534786'

ALL_COLUMNS = ['date','high','low','open','close','volume','quoteVolume','weightedAverage']

COLUMNS_FEATURES = ['high','low','open','close','volume','quoteVolume','weightedAverage']
COLUMN_TARGET = ['weightedAverage']

FEATURE_LEN = 2
PRED_LEN = 2

def df_to_series():
	df = df_from_pickle(FILENAME)[:20]

	features = df[COLUMNS_FEATURES]
	target = df[COLUMN_TARGET]

	series = []
	for i in range(len(df)-FEATURE_LEN-PRED_LEN):
		series.append([(features[i:i+FEATURE_LEN].values.tolist()), target[i+FEATURE_LEN:i+FEATURE_LEN+PRED_LEN].values.tolist()])

	return series

def serie_to_input_tensor(serie): 
	return torch.FloatTensor(serie[0])

	# for i, timestep in enumerate(vec):
	# 	for j, element in enumerate(timestep[0]):
	# 		vec[i][0][j] = series[0][i][j]
	# return vec

def serie_to_target_tensor(serie):
	return torch.FloatTensor(serie[1])

series = df_to_series()

feature_target_pairs = []
for serie in series:
	feature_target_pairs.append([serie_to_input_tensor(serie), serie_to_target_tensor(serie)])

print(feature_target_pairs)