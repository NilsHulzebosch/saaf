from coin import Coin
from wallet import Wallet
from tradebot import Tradebot

if __name__ == "__main__":
	
	wallet = Wallet(coins=[
		Coin(name='USDT', volume=0.), 
		Coin(name='STR'	, volume=1082.), 
		Coin(name='BTC' , volume=0.)
		])

	tradebot = Tradebot(wallet = wallet, base_currency = 'USDT', quote_currency = 'STR', delta_sell = 0.95)
	tradebot.trade_loop()