import os
import time
import datetime
import pandas as pd
import csv

CURRENCY_PAIR = 'USDT_BTC'
START_DATE = '1388534400'	# unix timestamp for 2014.01.01
CANDLESTICK_PERIOD = '300'	# candlestick period in seconds; valid values are 300, 900, 1800, 7200, 14400, and 86400

# URL to get API data:
FETCH_URL = 'https://poloniex.com/public?command=returnChartData&currencyPair='+CURRENCY_PAIR+'&start='+START_DATE+'&period='+CANDLESTICK_PERIOD 

DATA_DIR = "data"
FILE_NAME = "data.csv"
COLUMNS = ["date","high","low","open","close","volume","quoteVolume","weightedAverage"]

def timestamp_to_datetime(timestamp):
	return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

def datetime_to_timestamp(timestring): # Input string of the form '%Y-%m-%d %H:%M:%S' or '%Y-%m-%d'
	if len(timestring) <= 11:
		return time.mktime(datetime.datetime.strptime(timestring, '%Y-%m-%d').timetuple())
	else:
		print('yes')
		return time.mktime(datetime.datetime.strptime(timestring, '%Y-%m-%d %H:%M:%S').timetuple())	

def main():
	if not os.path.exists(DATA_DIR):
		os.mkdir(DATA_DIR)

	df = pd.read_json(FETCH_URL)

	df.to_csv(path_or_buf=DATA_DIR+'/'+ FILE_NAME, sep=',', na_rep='', float_format=None, 
		columns=None, header=True, index=True, index_label=None, mode='w', 
		encoding=None, compression=None, quoting=None, quotechar='"', 
		line_terminator='\n', chunksize=None, tupleize_cols=None, 
		date_format=None, doublequote=True, escapechar=None, decimal='.')

if __name__ == '__main__':
	main()