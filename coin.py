class Coin:

	def __init__(self, name=None, volume=0):
		self.name = name
		self.volume = volume

	def __repr__(self):
		return self.name

	__str__ = __repr__

	def content(self):
		return self.name + ': ' + str(self.volume)