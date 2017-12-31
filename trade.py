from get_polo_data import hist_ticker
import time
class Market_situation:

	def __init__(self, ticker_df=None, hist_df=None):

		self.ticker_df = ticker_df
		self.hist_df = hist_df

		self.name = ticker_df.name
		self.baseVolume = ticker_df['baseVolume']
		self.high24hr = ticker_df['high24hr']
		self.highestBid = ticker_df['highestBid']
		self.id = ticker_df['id']
		self.isFrozen = ticker_df['isFrozen']
		self.last = ticker_df['last']
		self.low24hr = ticker_df['low24hr']
		self.lowestAsk = ticker_df['lowestAsk']
		self.percentChange = ticker_df['percentChange']
		self.quoteVolume = ticker_df['quoteVolume']

	def __repr__(self):
		return str(self.ticker_df)

def main():

	stack = []

	i = 0
	while i < 10:
		time.sleep(1)
		i += 1

		hist_df, ticker_df = hist_ticker()

		previous_situation = 0
		if len(stack) > 0:
			previous_situation = stack.pop()

		current_situation = Market_situation(ticker_df=ticker_df, hist_df=hist_df).last

		print("Current ", current_situation)
		print("previous_situation ", previous_situation)

		if current_situation >= previous_situation:
			print('HODL')
		else:
			print('SELL')

		stack.append(current_situation)


if __name__ == '__main__':
	main()