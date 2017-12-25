from get_polo_data import df_from_pickle

FILENAME = 'data_USDT_BTC_start_2014-01-01 01:00:00_period_300_retrieved_2017-12-25 16:51:38.534786'

ALL_COLUMNS = ['date','high','low','open','close','volume','quoteVolume','weightedAverage']

COLUMNS_FEATURES = ['high','low','open','close','volume','quoteVolume','weightedAverage']
COLUMN_TARGET = 'weightedAverage'

FEATURE_LEN = 2
PRED_LEN = 2

def df_to_series():
	df = df_from_pickle(FILENAME)[:20]

	features = df[COLUMNS_FEATURES]
	target = df[COLUMN_TARGET]

	series = []
	for i in range(len(df)-FEATURE_LEN-PRED_LEN):
		series.append([(features[i:i+FEATURE_LEN].values.tolist()), list(target[i+FEATURE_LEN:i+FEATURE_LEN+PRED_LEN])])

	return series

