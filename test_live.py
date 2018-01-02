from get_polo_data import hist_ticker
from coin import Coin
from wallet import Wallet
import time
import copy

BASE_CURRENCY = 'USDT'
QUOTE_CURRENCY = 'STR'
FEE = 0.0025

SLEEP = 0

DELTA_SELL = 0.96
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

	i = 0
	while True:
		i += 1
		time.sleep(SLEEP)

		previous_price = stack.pop(0)
		_, ticker_df = hist_ticker()
		current_price = ticker_df['last']
		stack.append(current_price)

		if current_price > maximum_price:
			maximum_price = current_price

		if print_trace == 'all':
			print('-------------------------------------')
			print('In sell loop, iteration            ', i)
			print('Previously bought at               ', init_price)
			print('Current_price                      ', current_price)
			print()
			print('Maximum                            ', maximum_price)
			print('Going to sell when below           ', maximum_price*DELTA_SELL)
			print()
			init_base_volume = wallet.coin(QUOTE_CURRENCY).volume*init_price
			est_base_vol = wallet.coin(QUOTE_CURRENCY).volume*(1-FEE)*maximum_price*DELTA_SELL
			print('Init base volume                   ', init_base_volume)
			print('Estimated base volume after trade  ', est_base_vol)
			print('Estimated base profit              ', est_base_vol - init_base_volume)
			print()
			print(wallet)
			print()

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

	i = 0
	while True:
		i+=1
		time.sleep(SLEEP)

		previous_price = stack.pop(0)
		_, ticker_df = hist_ticker()
		current_price = ticker_df['last']
		stack.append(current_price)

		if current_price < minimum_price:
			minimum_price = current_price

		if print_trace == 'all':
			print('-------------------------------------')
			print('In buy loop, iteration              ', i)
			print('Previously sold at                  ', init_price)
			print('Current_price                       ', current_price)
			print()
			print('Minimum                             ', minimum_price)
			print('Going to buy when above             ', minimum_price*DELTA_BUY)
			print()
			init_quote_volume = wallet.coin(BASE_CURRENCY).volume/init_price
			est_quote_vol = wallet.coin(BASE_CURRENCY).volume/((1-FEE)*minimum_price*DELTA_BUY)
			print('Init quote volume                   ', init_quote_volume)
			print('Estimated quote volume after trade  ', est_quote_vol)
			print('Estimated quote profit              ', est_quote_vol - init_quote_volume)
			print()
			print(wallet)
			print()

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
	Coin(name='USDT', volume=0.), 
	Coin(name='STR'	, volume=1082.), 
	Coin(name='BTC' , volume=0.)
	])

# hist_prices = []
# hist_df, _ = hist_ticker()
# for index, element in hist_df.iterrows():
# 	hist_prices.append(element['weightedAverage'])


hist_df, ticker_df = hist_ticker()
init_price = ticker_df['last']

init_base_volume = wallet.coin(BASE_CURRENCY).volume 

print(wallet)

buy_price = 0.13

while True:
	sell_price = sell(init_price=buy_price, print_trace='all')
	buy_price = buy(init_price=sell_price, print_trace='all')

print()
print(wallet)