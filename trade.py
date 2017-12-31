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

FEE = 0.0025
TRADE_VOL = 0.1
DELTA = 0.96

def main():

	stack = []

	buy_price = 0
	maximum_price = 0

	i = 0
	while i < 10:
		time.sleep(0.5)
		i += 1

		hist_df, ticker_df = hist_ticker()


		current_situation = Market_situation(ticker_df=ticker_df, hist_df=hist_df).last
		total_fee = current_situation*FEE*TRADE_VOL

		previous_situation = 0
		if len(stack) > 0:
			previous_situation = stack.pop()
		else:
			buy_price = current_situation

		print('-------------------------')

		if current_situation >= maximum_price:
			maximum_price = current_situation

		print('Previous   ', previous_situation)
		print('Current    ', current_situation)
		print()

		buy_value = buy_price*TRADE_VOL + buy_price*TRADE_VOL*FEE
		sell_value = current_situation*TRADE_VOL - current_situation*TRADE_VOL*FEE
		profit = sell_value - buy_value

		print('Buy value  ', buy_value)
		print('Sell value ', sell_value)
		print('Profit     ', profit)
		print()

		stack.append(current_situation) 


		if current_situation >= previous_situation: # Increasing
			print('H O D L')
		else:										# Decreasing
			current_situation < maximum_price*DELTA
			print('S E L L')
		print()



if __name__ == '__main__':
	main()