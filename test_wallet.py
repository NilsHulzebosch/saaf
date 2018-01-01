from get_polo_data import hist_ticker
import time
import copy

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

class Coin:

	def __init__(self, name=None, volume=0):
		self.name = name
		self.volume = volume

	def __repr__(self):
		return self.name

	__str__ = __repr__

	def content(self):
		return self.name + ': ' + str(self.volume)

class Wallet:

	def __init__(self, coins=[]):
		self.coins = coins

	def __repr__(self):
		return str([x.content() for x in self.coins])

	def coin(self, name=None):
		for coin in self.coins:
			if coin.name == name:
				return coin


BASE_CURRENCY = 'USDT'
QUOTE_CURRENCY = 'STR'

FEE = 0.0025
SLEEP = 0

SELL_DELTA = 1
BUY_DELTA = 2-SELL_DELTA

wallet = Wallet(coins=[
	Coin(name='USDT', volume=100), 
	Coin(name='STR'	, volume=0), 
	Coin(name='BTC' , volume=0)
	])

hist_prices = []
hist_df, _ = hist_ticker()
for index, element in hist_df.iterrows():
	hist_prices.append(element['weightedAverage'])

current_price = 0

quote_vol = wallet.coin(QUOTE_CURRENCY).volume
base_vol = wallet.coin(BASE_CURRENCY).volume

def trade(price, base_vol=None, base_currency=BASE_CURRENCY, quote_currency=QUOTE_CURRENCY):
	base_coin = wallet.coin(base_currency)
	if base_vol == None or base_vol > base_coin.volume:
		base_vol = base_coin.volume

	quote_vol = (base_vol / price) * (1-FEE)

	wallet.coin(base_currency).volume -= base_vol
	wallet.coin(quote_currency).volume += quote_vol

def sell(initial_price=0, print_trace=False):

	stack = [initial_price] # Store previous price

	buy_price = initial_price
	maximum_price = initial_price

	i = 0
	while len(hist_prices)>0:
		time.sleep(SLEEP)
		i += 1

		global current_price
		current_price = hist_prices.pop(0)
		previous_price = stack.pop(0)

		if current_price >= maximum_price: # Set maximum
			maximum_price = current_price

		buy_base_value = buy_price*quote_vol
		sell_base_value = (1-FEE)*current_price*quote_vol

		value_profit = sell_base_value - buy_base_value

		new_quote_vol = (1-FEE)*(current_price*quote_vol / buy_price)
		volume_profit = new_quote_vol - quote_vol

		if print_trace:
			print('-------------------------')
			print('Sell counter      ', i)
			print()
			print('Bought at         ', buy_price)
			print()
			print('Previous price    ', previous_price)
			print('Current price     ', current_price)
			print()
			print('Buy base value    ', buy_base_value)
			print('Sell base value   ', sell_base_value)
			print()
			print('Quote volume      ', quote_vol)
			print('New quote volume  ', new_quote_vol)
			print()
			print('Value profit      ', value_profit)
			print('Volume profit     ', volume_profit)
			print()
			print('Total base profit ', wallet.coin(BASE_CURRENCY).volume - init_wallet.coin(BASE_CURRENCY).volume)
			print('Total quote profit', wallet.coin(QUOTE_CURRENCY).volume - init_wallet.coin(QUOTE_CURRENCY).volume)
			print()

		stack.append(current_price) 

		if current_price >= previous_price: # Increasing
			if print_trace:
				print('Going to sell at  ', maximum_price*SELL_DELTA)
				print()
				print('H O D L')
				print()

		else:
			if current_price <= maximum_price*SELL_DELTA and value_profit > 0:
				print('S O L D at       ', current_price)
				print()
				print(' --- S O L D --- ')
				print()
				trade(price=1/current_price, base_currency=QUOTE_CURRENCY, quote_currency=BASE_CURRENCY)

				return current_price

			elif print_trace:
				print('Going to sell at  ', maximum_price*SELL_DELTA)
				print()
				print('Oooooooh hodl')
				print()
	return 0, []

def buy(initial_price=0, print_trace=False):
	stack = [initial_price] # Store previous price

	minimum_price = initial_price

	i = 0
	while len(hist_prices)>0:
		time.sleep(SLEEP)
		i += 1

		global current_price
		current_price = hist_prices.pop(0)

		previous_price = stack.pop(0)

		if current_price <= minimum_price: # Set minimum
			minimum_price = current_price

		new_base_vol = (1-FEE)*((initial_price*base_vol)/current_price)

		buy_value = current_price*BUY_DELTA*new_base_vol*(1-FEE)

		if print_trace:
			print('-------------------------')
			print('Buy counter       ', i)
			print('Sold at           ', initial_price)
			print()
			print('Previous price    ', previous_price)
			print('Current price     ', current_price)
			print()
			print('Buy value         ', buy_value)
			print('Curr trade volume ', base_vol)
			print('New trade volume  ', new_base_vol)
			print()
			print('Total base profit ', wallet.coin(BASE_CURRENCY).volume - init_wallet.coin(BASE_CURRENCY).volume)
			print('Total quote profit', wallet.coin(QUOTE_CURRENCY).volume - init_wallet.coin(QUOTE_CURRENCY).volume)
			print()

		stack.append(current_price) 

		if current_price <= previous_price: # Increasing
			if print_trace:
				print('Going to buy at   ', minimum_price*BUY_DELTA)
				print()
				print('N I K S')
				print()
		else:
			if current_price >= minimum_price*BUY_DELTA:
				trade(price=current_price)

				print('Bought at         ', current_price)
				print()
				print(' --- B U Y --- ')
				print()

				return current_price
			else:
				if print_trace:
					print('Going to buy at   ', minimum_price*BUY_DELTA)
					print()
					print('Oooooh niks')
					print()
	return 0, []

def main():

	total_base_profit = 0
	total_quote_profit = 0

	init_wallet = copy.deepcopy(wallet)

	init_buy_price  = hist_prices.pop(0)
	buy_price = init_buy_price

	trade(init_buy_price, base_vol=None)
	print(wallet)

	while len(hist_prices) > 0:
		sell_price = sell(initial_price = buy_price)
		base_vol = wallet.coin(BASE_CURRENCY).volume
		print(wallet)

		buy_price = buy(initial_price = sell_price)
		quote_vol = wallet.coin(QUOTE_CURRENCY).volume
		print(wallet)

	print(wallet)
	total_base_profit = wallet.coin(BASE_CURRENCY).volume - init_wallet.coin(BASE_CURRENCY).volume
	total_quote_profit = wallet.coin(QUOTE_CURRENCY).volume - init_wallet.coin(QUOTE_CURRENCY).volume

	print('Total base profit ', wallet.coin(QUOTE_CURRENCY).volume*current_price - init_wallet.coin(BASE_CURRENCY).volume)
	print('Total quote profit', wallet.coin(QUOTE_CURRENCY).volume - init_wallet.coin(QUOTE_CURRENCY).volume)

if __name__ == '__main__':
	main()