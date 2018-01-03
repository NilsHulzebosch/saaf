from coin import Coin
from wallet import Wallet
from tradebot import Tradebot

if __name__ == "__main__":
	
	wallet = Wallet(coins=[
		Coin(name='USDT', volume=100.), 
		Coin(name='STR'	, volume=0.), 
		Coin(name='BTC' , volume=0.)
		])

	tradebot = Tradebot(wallet = wallet, base_currency = 'USDT', quote_currency = 'STR')
	tradebot.trade_loop()