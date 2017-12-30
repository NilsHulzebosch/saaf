import os
import time
import datetime
import pandas as pd
import pickle

CURRENCY_PAIR = 'USDT_BTC'
START_DATE = '1388534400'	# unix timestamp for 2014.01.01
CANDLESTICK_PERIOD = '300'	# candlestick period in seconds; valid values are 300, 900, 1800, 7200, 14400, and 86400

COLUMNS = ['date','high','low','open','close','volume','quoteVolume','weightedAverage']

def timestamp_to_datetime(timestamp):
	return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

def datetime_to_timestamp(timestring): # Input string of the form '%Y-%m-%d %H:%M:%S' or '%Y-%m-%d'
	if len(timestring) <= 11:
		return str(time.mktime(datetime.datetime.strptime(timestring, '%Y-%m-%d').timetuple()))
	else:
		return str(time.mktime(datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S').timetuple()))

DATA_DIR = 'data'
FILE_NAME = 'data_'+CURRENCY_PAIR+'_start_'+str(timestamp_to_datetime(START_DATE))+\
	'_period_'+CANDLESTICK_PERIOD+'_retrieved_'+str(datetime.datetime.now())

def fetch_data_to_pickle(start_date=START_DATE, end_date=None):
	if not os.path.exists(DATA_DIR):
		os.mkdir(DATA_DIR)

	# URL to get API data:
	FETCH_URL = 'https://poloniex.com/public?command=returnChartData&currencyPair='+\
		CURRENCY_PAIR+'&start='+start_date+'&period='+CANDLESTICK_PERIOD 

	df = pd.read_json(FETCH_URL)

	print(df)

	df.to_pickle(path=DATA_DIR+'/'+FILE_NAME)

def df_from_pickle(filename):
	return pickle.load(open(DATA_DIR+'/'+filename, "rb" ))


def main():
	fetch_data_to_pickle(start_date=datetime_to_timestamp('2017-12-30 19:00:00'))

if __name__ == '__main__':
	main()