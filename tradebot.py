from get_polo_data import ticker
from coin import Coin
from wallet import Wallet
import time
import copy

BASE_CURRENCY = 'BTC'
QUOTE_CURRENCY = 'STR'
FEE = 0.0025

SLEEP = 0

DELTA_SELL = 1
DELTA_BUY = 2 - DELTA_SELL

class Tradebot:

	def __init__(self, 
		base_currency=BASE_CURRENCY,
		quote_currency=QUOTE_CURRENCY,
		fee = FEE,
		sleep = SLEEP,
		delta_sell = DELTA_SELL,
		delta_buy = DELTA_BUY,
		wallet=Wallet()
		):

		self.BASE_CURRENCY = base_currency
		self.QUOTE_CURRENCY = quote_currency
		self.FEE = fee
		self.SLEEP = sleep
		self.DELTA_SELL = delta_sell
		self.DELTA_BUY = delta_buy

		self.wallet = wallet
		self.init_wallet = copy.deepcopy(wallet) # Save initial situation

	def trade(self, 
		price, 
		base_vol=None, 
		base_currency=BASE_CURRENCY, 
		quote_currency=QUOTE_CURRENCY
		):

		base_coin = self.wallet.coin(base_currency)

		if base_vol == None or base_vol > base_coin.volume:
			base_vol = base_coin.volume # Maximum amount in wallet

		quote_vol = (base_vol / price) * (1-self.FEE)

		self.wallet.coin(base_currency).volume -= base_vol
		self.wallet.coin(quote_currency).volume += quote_vol

	def sell(self, init_price=0, print_trace=None):

		stack = [init_price]
		maximum_price = init_price

		i = 0
		while True:
			i += 1

			time.sleep(self.SLEEP)

			previous_price = stack.pop(0)

			current_price = ticker()['last']

			stack.append(current_price)

			if current_price > maximum_price:
				maximum_price = current_price

			if print_trace == 'all':	

				base_volume = self.wallet.coin(QUOTE_CURRENCY).volume*init_price
				est_base_vol = self.wallet.coin(QUOTE_CURRENCY).volume*(1-self.FEE)*maximum_price*self.DELTA_SELL

				print('-------------------------------------')
				print('In sell loop, iteration            ', i)
				print('Previously bought at               ', init_price, self.BASE_CURRENCY)
				print('Current price                      ', current_price, self.BASE_CURRENCY)
				print()
				print('Maximum                            ', maximum_price, self.BASE_CURRENCY)
				print('Going to sell when below           ', maximum_price*self.DELTA_SELL, self.BASE_CURRENCY)
				print()
				print('Init base volume                   ', base_volume, self.BASE_CURRENCY)
				print('Estimated base volume after trade  ', est_base_vol, self.BASE_CURRENCY)
				print('Estimated base profit              ', est_base_vol - base_volume, self.BASE_CURRENCY)
				print()
				print('Init est quote volume              ', base_volume/current_price, self.QUOTE_CURRENCY)
				print('Estimated quote volume after trade ', est_base_vol/current_price, self.QUOTE_CURRENCY)
				print('Estimated quote profit             ', (est_base_vol - base_volume)/current_price, self.QUOTE_CURRENCY)
				print()
				print('Total base profit                  ', self.base_profit(price=current_price), self.BASE_CURRENCY)
				print('Total quote profit                 ', self.quote_profit(price=current_price), self.QUOTE_CURRENCY)
				print()
				print('Wallet                             ', self.wallet)
				print()

			if current_price >= previous_price:
				if print_trace == 'all':
					print('H O D L')

			elif current_price < maximum_price*self.DELTA_SELL:
				self.trade(
					price=1/current_price, 
					base_vol=self.wallet.coin(self.QUOTE_CURRENCY).volume, 
					base_currency=self.QUOTE_CURRENCY, 
					quote_currency=self.BASE_CURRENCY
					)

				if print_trace == 'action' or print_trace == 'all':
					print('S E L L')
					print(self.wallet)
					print()

				return current_price

			else:
				if print_trace == 'all':
					print('Oooooh hodl')

	def buy(self, init_price=0, print_trace=None):

		stack = [init_price]
		minimum_price = init_price

		i = 0
		while True:
			i+=1

			time.sleep(self.SLEEP)

			previous_price = stack.pop(0)

			current_price = ticker()['last']

			stack.append(current_price)

			if current_price < minimum_price:
				minimum_price = current_price

			if print_trace == 'all':

				quote_volume = self.wallet.coin(self.BASE_CURRENCY).volume/init_price
				est_quote_vol = self.wallet.coin(self.BASE_CURRENCY).volume/((1-self.FEE)*minimum_price*self.DELTA_BUY)

				print('-------------------------------------')
				print('In buy loop, iteration             ', i)
				print('Previously sold at                 ', init_price, self.BASE_CURRENCY)
				print('Current price                      ', current_price, self.BASE_CURRENCY)
				print()
				print('Minimum                            ', minimum_price, self.BASE_CURRENCY)
				print('Going to buy when above            ', minimum_price*self.DELTA_BUY, self.BASE_CURRENCY)
				print()
				print('Init quote volume                  ', quote_volume, self.QUOTE_CURRENCY)
				print('Estimated quote volume after trade ', est_quote_vol, self.QUOTE_CURRENCY)
				print('Estimated quote profit             ', est_quote_vol - quote_volume, self.QUOTE_CURRENCY)
				print()
				print('Init est base volume               ', quote_volume*current_price, self.BASE_CURRENCY)
				print('Estimated base volume after trade  ', est_quote_vol*current_price, self.BASE_CURRENCY)
				print('Estimated base profit              ', (est_quote_vol - quote_volume)*current_price, self.BASE_CURRENCY)
				print()
				print('Total base profit                  ', self.base_profit(price=current_price), self.BASE_CURRENCY)
				print('Total quote profit                 ', self.quote_profit(price=current_price), self.QUOTE_CURRENCY)
				print()
				print('Wallet                             ', self.wallet)
				print()

			if current_price <= previous_price:
				if print_trace == 'all':
					print('N I K S')

			elif current_price > minimum_price*self.DELTA_BUY:
				self.trade(
					price=current_price, 
					base_vol=self.wallet.coin(self.BASE_CURRENCY).volume
					)

				if print_trace == 'action' or print_trace == 'all':
					print('B U Y')
					print(self.wallet)
					print()
				
				return current_price

			else:
				if print_trace == 'all':
					print('Oooooh niks')

	def base_profit(self,
		price=1, 
		init_wallet=None, 
		wallet=None, 
		base_currency=BASE_CURRENCY, 
		quote_currency=QUOTE_CURRENCY
		):

		if init_wallet == None:
			init_wallet = self.init_wallet

		if wallet == None:
			wallet = self.wallet

		return wallet.coin(base_currency).volume - \
			init_wallet.coin(base_currency).volume + \
			wallet.coin(quote_currency).volume*price - \
			init_wallet.coin(quote_currency).volume*price

	def quote_profit(self,
		price=1, 
		init_wallet=None, 
		wallet=None, 
		base_currency=BASE_CURRENCY, 
		quote_currency=QUOTE_CURRENCY
		):

		if init_wallet == None:
			init_wallet = self.init_wallet

		if wallet == None:
			wallet = self.wallet

		return wallet.coin(base_currency).volume/price - \
			init_wallet.coin(base_currency).volume/price + \
			wallet.coin(quote_currency).volume - \
			init_wallet.coin(quote_currency).volume

	def trade_loop(self, init_buy_price=ticker()['last'], wallet=None):
		if wallet == None:
			wallet = self.wallet

		buy_price = init_buy_price

		while True: # Infinite trade loop
			sell_price = self.sell(init_price=buy_price, print_trace='all')
			buy_price = self.buy(init_price=sell_price, print_trace='all')