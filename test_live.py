from get_polo_data import ticker
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

		ticker_df = ticker()
		current_price = ticker_df['last']

		stack.append(current_price)

		if current_price > maximum_price:
			maximum_price = current_price

		if print_trace == 'all':	

			base_volume = wallet.coin(QUOTE_CURRENCY).volume*init_price
			est_base_vol = wallet.coin(QUOTE_CURRENCY).volume*(1-FEE)*maximum_price*DELTA_SELL

			print('-------------------------------------')
			print('In sell loop, iteration            ', i)
			print('Previously bought at               ', init_price)
			print('Current price                      ', current_price)
			print()
			print('Maximum                            ', maximum_price)
			print('Going to sell when below           ', maximum_price*DELTA_SELL)
			print()
			print('Init base volume                   ', base_volume)
			print('Estimated base volume after trade  ', est_base_vol)
			print('Estimated base profit              ', est_base_vol - base_volume)
			print()
			print('Total base profit                  ', 
				base_profit(price=current_price, init_wallet=init_wallet, wallet=wallet))
			print('Total quote profit                 ', 
				quote_profit(price=current_price, init_wallet=init_wallet, wallet=wallet))
			print(wallet)
			print()

		if current_price > previous_price:
			if print_trace == 'all':
				print('H O D L')

		elif current_price < maximum_price*DELTA_SELL:
			trade(
				price=1/current_price, 
				base_vol=wallet.coin(QUOTE_CURRENCY).volume, 
				base_currency=QUOTE_CURRENCY, 
				quote_currency=BASE_CURRENCY
				)

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

		ticker_df = ticker()
		current_price = ticker_df['last']

		stack.append(current_price)

		if current_price < minimum_price:
			minimum_price = current_price

		if print_trace == 'all':

			quote_volume = wallet.coin(BASE_CURRENCY).volume/init_price
			est_quote_vol = wallet.coin(BASE_CURRENCY).volume/((1-FEE)*minimum_price*DELTA_BUY)

			print('-------------------------------------')
			print('In buy loop, iteration              ', i)
			print('Previously sold at                  ', init_price)
			print('Current price                       ', current_price)
			print()
			print('Minimum                             ', minimum_price)
			print('Going to buy when above             ', minimum_price*DELTA_BUY)
			print()
			print('Init quote volume                   ', quote_volume)
			print('Estimated quote volume after trade  ', est_quote_vol)
			print('Estimated quote profit              ', est_quote_vol - quote_volume)
			print()
			print('Total base profit                   ', 
				base_profit(price=current_price, init_wallet=init_wallet, wallet=wallet))
			print('Total quote profit                  ', 
				quote_profit(price=current_price, init_wallet=init_wallet, wallet=wallet))
			print(wallet)
			print()

		if current_price < previous_price:
			if print_trace == 'all':
				print('N I K S')

		elif current_price > minimum_price*DELTA_BUY:
			trade(
				price=current_price, 
				base_vol=wallet.coin(BASE_CURRENCY).volume
				)

			if print_trace == 'action' or print_trace == 'all':
				print('B U Y')
				print(wallet)
				print()
			
			return current_price

		else:
			if print_trace == 'all':
				print('Oooooh niks')

def base_profit(
	price=1, 
	init_wallet=Wallet(), 
	wallet=Wallet(), 
	base_currency=BASE_CURRENCY, 
	quote_currency=QUOTE_CURRENCY
	):
	return wallet.coin(BASE_CURRENCY).volume - \
		init_wallet.coin(BASE_CURRENCY).volume + \
		wallet.coin(QUOTE_CURRENCY).volume*price - \
		init_wallet.coin(QUOTE_CURRENCY).volume*price

def quote_profit(
	price=1, 
	init_wallet=Wallet(), 
	wallet=Wallet(), 
	base_currency=BASE_CURRENCY, 
	quote_currency=QUOTE_CURRENCY
	):
	return wallet.coin(BASE_CURRENCY).volume/price - \
		init_wallet.coin(BASE_CURRENCY).volume/price + \
		wallet.coin(QUOTE_CURRENCY).volume - \
		init_wallet.coin(QUOTE_CURRENCY).volume

wallet = Wallet(coins=[
	Coin(name='USDT', volume=0.), 
	Coin(name='STR'	, volume=1082.), 
	Coin(name='BTC' , volume=0.)
	])

init_wallet = copy.deepcopy(wallet) # Save initial situation

buy_price = 0.13

while True: # Infinite trade loop
	sell_price = sell(init_price=buy_price, print_trace='all')
	buy_price = buy(init_price=sell_price, print_trace='all')