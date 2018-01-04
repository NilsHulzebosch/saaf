class Wallet:

	def __init__(self, coins = []):
		self.coins = coins

	def __repr__(self):
		return str([x.content() for x in self.coins])

	def coin(self, name = None):
		for coin in self.coins:
			if coin.name == name:
				return coin