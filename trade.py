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
DELTA = 1#0.96
SLEEP = 0.5
total_profit = 0.


def sell(initial_price=0, print_trace=False):

	stack = [initial_price]

	buy_price = initial_price
	maximum_price = initial_price

	i = 0
	while True:
		time.sleep(SLEEP)
		i += 1

		hist_df, ticker_df = hist_ticker()
		current_price = Market_situation(ticker_df=ticker_df, hist_df=hist_df).last

		previous_situation = stack.pop()

		if current_price >= maximum_price: # Set maximum
			maximum_price = current_price

		buy_value = buy_price*TRADE_VOL + buy_price*TRADE_VOL*FEE
		sell_value = current_price*TRADE_VOL - current_price*TRADE_VOL*FEE
		profit = sell_value - buy_value

		if print_trace:
			print('-------------------------')
			print('Sell counter ', i)
			print('Previous     ', previous_situation)
			print('Current      ', current_price)
			print()

			print('Buy value    ', buy_value)
			print('Sell value   ', sell_value)
			print('Profit       ', profit)
			print()
			print('Total_profit ', total_profit)
			print()

		stack.append(current_price) 

		if current_price >= previous_situation: # Increasing
			print('H O D L')

		else:
			if current_price < maximum_price*DELTA:
				print('curr ', current_price)
				print('max_d', maximum_price*DELTA)
				print('max  ', maximum_price)
				print()
				print('S E L L')
				global total_profit
				total_profit += profit
				return current_price
		print()

def buy(initial_price=0, print_trace=False):
	stack = [initial_price]

	minimum_price = initial_price

	i = 0
	while True:
		time.sleep(SLEEP)
		i += 1

		hist_df, ticker_df = hist_ticker()
		current_price = Market_situation(ticker_df=ticker_df, hist_df=hist_df).last

		previous_situation = stack.pop()

		if current_price <= minimum_price: # Set maximum
			minimum_price = current_price

		buy_value = current_price*TRADE_VOL - current_price*TRADE_VOL*FEE

		if print_trace:
			print('-------------------------')
			print('Buy counter', i)
			print('Previous   ', previous_situation)
			print('Current    ', current_price)
			print()

			print('Buy value  ', buy_value)
			print()
			print('Total_profit ', total_profit)
			print()

		stack.append(current_price) 

		if current_price <= previous_situation: # Increasing
			print('N I K S')
		else:
			if current_price > minimum_price*DELTA:
				print('curr ', current_price)
				print('min_d', minimum_price*DELTA)
				print('min  ', minimum_price)
				print()
				print('B U Y')
				return current_price
		print()

def main():
	hist_df, ticker_df = hist_ticker()
	buy_price = Market_situation(ticker_df=ticker_df, hist_df=hist_df).last

	while True:
		sell_price = sell(initial_price=buy_price, print_trace=True)
		buy_price = buy(initial_price=sell_price, print_trace=True)

if __name__ == '__main__':
	main()