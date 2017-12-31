from get_polo_data import hist_ticker

def main():
	hist_df, ticker_df = hist_ticker()

	print(hist_df)
	print(ticker_df)

if __name__ == '__main__':
	main()