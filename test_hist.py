from get_polo_data import hist_ticker
from coin import Coin
from wallet import Wallet
import time
import copy

BASE_CURRENCY = 'USDT'
QUOTE_CURRENCY = 'BTC'
FEE = 0.0025

DELTA_SELL = 0.964
DELTA_BUY = 2 - DELTA_SELL

def trade(price, base_vol=None, base_currency=BASE_CURRENCY, quote_currency=QUOTE_CURRENCY):
	base_coin = wallet.coin(base_currency)

	if base_vol == None or base_vol > base_coin.volume:
		base_vol = base_coin.volume # Maximum amount in wallet

	quote_vol = (base_vol / price) * (1-FEE)

	wallet.coin(base_currency).volume -= base_vol
	wallet.coin(quote_currency).volume += quote_vol

def sell(init_price=0, print_trace=None):
	stack = [init_price]
	maximum_price = init_price

	while len(hist_prices) > 0:

		previous_price = stack.pop(0)
		current_price = hist_prices.pop(0)
		stack.append(current_price)

		if current_price > maximum_price:
			maximum_price = current_price

		if current_price > previous_price:
			if print_trace == 'all':
				print('H O D L')
		elif current_price < maximum_price*DELTA_SELL:
			trade(price=1/current_price, base_vol=wallet.coin(QUOTE_CURRENCY).volume, base_currency=QUOTE_CURRENCY, quote_currency=BASE_CURRENCY)
			if print_trace == 'action' or print_trace == 'all':
				print('S E L L')
				print(wallet)
				print()
			return current_price
		else:
			if print_trace == 'all':
				print('Oooooh hodl')

def buy(init_price=0, print_trace=None):
	stack = [init_price]
	minimum_price = init_price

	while len(hist_prices) > 0:

		previous_price = stack.pop(0)
		current_price = hist_prices.pop(0)
		stack.append(current_price)

		if current_price < minimum_price:
			minimum_price = current_price

		if current_price < previous_price:
			if print_trace == 'all':
				print('N I K S')

		elif current_price > minimum_price*DELTA_BUY:
			trade(price=current_price, base_vol=wallet.coin(BASE_CURRENCY).volume)
			if print_trace == 'action' or print_trace == 'all':
				print('B U Y')
				print(wallet)
				print()
			
			return current_price
		else:
			if print_trace == 'all':
				print('Oooooh niks')

wallet = Wallet(coins=[
	Coin(name='USDT', volume=100.), 
	Coin(name='STR'	, volume=0.), 
	Coin(name='BTC' , volume=0.)
	])

hist_prices = []
hist_df, _ = hist_ticker()
for index, element in hist_df.iterrows():
	hist_prices.append(element['weightedAverage'])

init_price = hist_prices.pop(0)
init_base_volume = wallet.coin(BASE_CURRENCY).volume 

print(wallet)
trade(price=init_price, base_vol=init_base_volume) # Trade half of base volume
print(wallet)

buy_price = init_price

while len(hist_prices) > 0:
	sell_price = sell(init_price=buy_price)
	buy_price = buy(init_price=sell_price)

print()
print(wallet)
