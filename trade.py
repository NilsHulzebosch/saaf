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

def sell(initial_price=0):
	stack = [initial_price]

	buy_price = initial_price
	maximum_price = initial_price

	i = 0
	while True:
		time.sleep(0.5)
		i += 1

		hist_df, ticker_df = hist_ticker()
		current_price = Market_situation(ticker_df=ticker_df, hist_df=hist_df).last

		previous_situation = stack.pop()

		if current_price >= maximum_price: # Set maximum
			maximum_price = current_price

		print('-------------------------')
		print('Previous   ', previous_situation)
		print('Current    ', current_price)
		print()

		buy_value = buy_price*TRADE_VOL + buy_price*TRADE_VOL*FEE
		sell_value = current_price*TRADE_VOL - current_price*TRADE_VOL*FEE
		profit = sell_value - buy_value

		print('Buy value  ', buy_value)
		print('Sell value ', sell_value)
		print('Profit     ', profit)
		print()

		stack.append(current_price) 

		if current_price >= previous_situation: # Increasing
			print('H O D L')
		else:
			if current_price < maximum_price*DELTA:
				print('curr ', current_price)
				print('max_d', maximum_price*DELT)
				print('max  ', maximum_price)

				print('S E L L')
				return current_price
		print()

def buy(initial_price=0):
	stack = [initial_price]

	minimum_price = initial_price

	i = 0
	while True:
		time.sleep(0.5)
		i += 1

		hist_df, ticker_df = hist_ticker()
		current_price = Market_situation(ticker_df=ticker_df, hist_df=hist_df).last

		previous_situation = stack.pop()

		if current_price <= minimum_price: # Set maximum
			minimum_price = current_price

		print('-------------------------')
		print('Previous   ', previous_situation)
		print('Current    ', current_price)
		print()

		buy_value = current_price*TRADE_VOL - current_price*TRADE_VOL*FEE

		print('Buy value  ', buy_value)
		print()

		stack.append(current_price) 

		if current_price <= previous_situation: # Increasing
			print('H O D L')
		else:
			if current_price > minimum_price*DELTA:
				print('curr ', current_price)
				print('max_d', minimum_price*DELT)
				print('max  ', minimum_price)

				print('B U Y')
				return current_price
		print()

def main():
	hist_df, ticker_df = hist_ticker()
	buy_price = Market_situation(ticker_df=ticker_df, hist_df=hist_df).last

	while True:
		sell_price = sell(initial_price=buy_price)
		buy_price = buy(initial_price=sell_price)

if __name__ == '__main__':
	main()