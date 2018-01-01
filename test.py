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
DELTA = 0.99 # The closer to one, the narrower the distance between current price and selling/buying price
DELTA_BUY = 2 - DELTA
SLEEP = 0

total_profit = 0.
total_volume_profit = 0.

investment = 100 # First currency of the pair

def sell(initial_price=0, print_trace=False, hist_prices=[]):

	stack = [initial_price] # Store previous price

	buy_price = initial_price
	maximum_price = initial_price

	i = 0
	while len(hist_prices)>0:
		time.sleep(SLEEP)
		i += 1

		current_price = hist_prices.pop(0)

		previous_price = stack.pop(0)

		if current_price >= maximum_price: # Set maximum
			maximum_price = current_price

		buy_value = buy_price*trade_vol
		sell_value = current_price*trade_vol - current_price*trade_vol*FEE
		profit = sell_value - buy_value
		volume_profit = trade_vol*profit / buy_value

		if print_trace:
			print('-------------------------')
			print('Sell counter      ', i)
			print()
			print('Bought at         ', buy_price)
			print()
			print('Previous price    ', previous_price)
			print('Current price     ', current_price)
			print()
			print('Buy value         ', buy_value)
			print('Sell value        ', sell_value)
			print('Trade volume      ', trade_vol)
			print()
			print('Profit            ', profit)
			print('Volume profit     ', volume_profit)
			print()
			print('Total profit      ', total_profit)
			print('Total vol profit  ', total_volume_profit)
			print()

		stack.append(current_price) 

		if current_price >= previous_price: # Increasing
			print('Going to sell at  ', maximum_price*DELTA)
			print()
			print('H O D L')

		else:
			if current_price <= maximum_price*DELTA:# and profit > 0:
				print('S O L D at       ', current_price)
				print()
				print(' --- S O L D --- ')

				global total_profit
				total_profit += profit

				global total_volume_profit
				total_volume_profit += volume_profit

				return current_price, hist_prices
			else:
				print('Going to sell at  ', maximum_price*DELTA)
				print()
				print('Oooooooh hodl')
		print()
	return 0, []

def buy(initial_price=0, print_trace=False, hist_prices=[]):
	stack = [initial_price] # Store previous price

	minimum_price = initial_price

	i = 0
	while len(hist_prices)>0:
		time.sleep(SLEEP)
		i += 1

		current_price = hist_prices.pop(0)

		previous_price = stack.pop(0)

		if current_price <= minimum_price: # Set minimum
			minimum_price = current_price

		new_trade_vol = trade_vol*initial_price / current_price*(1 - FEE)

		buy_value = current_price*new_trade_vol - current_price*new_trade_vol*FEE

		if print_trace:
			print('-------------------------')
			print('Buy counter       ', i)
			print('Sold at           ', initial_price)
			print()
			print('Previous price    ', previous_price)
			print('Current price     ', current_price)
			print()
			print('Buy value         ', buy_value)
			print('Curr trade volume ', trade_vol)
			print('New trade volume  ', new_trade_vol)
			print()
			print('Total profit      ', total_profit)
			print('Total vol profit  ', total_volume_profit)
			print()

		stack.append(current_price) 

		if current_price <= previous_price: # Increasing
			print('Going to buy at   ', minimum_price*DELTA_BUY)
			print()
			print('N I K S')
		else:
			if current_price >= minimum_price*DELTA:
				print('Bought at         ', current_price)
				print()
				print(' --- B U Y --- ')
				global trade_vol
				trade_vol = new_trade_vol
				return current_price, hist_prices
			else:
				print('Going to buy at   ', minimum_price*DELTA_BUY)
				print()
				print('Oooooh niks')
		print()
	return 0, []

def trade(hist_prices=[]):
	buy_price = hist_prices.pop(0)

	global init_trade_vol # initial trade volume based on investment substracted by fee
	init_trade_vol = investment / buy_price - FEE * investment / buy_price 

	global trade_vol
	trade_vol = init_trade_vol

	while len(hist_prices)>0: # Main trade loop
		sell_price, hist_prices = sell(initial_price=buy_price, print_trace=True, hist_prices=hist_prices) # Sell at optimum
		buy_price, hist_prices = buy(initial_price=sell_price, print_trace=True, hist_prices=hist_prices) # Buy at optimum

def main():
	hist_prices = []
	hist_df, _ = hist_ticker()
	for index, element in hist_df.iterrows():
		hist_prices.append(element['weightedAverage'])

	trade(hist_prices=hist_prices)

if __name__ == '__main__':
	main()