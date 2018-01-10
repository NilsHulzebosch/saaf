class Market_situation:

	def __init__(self, ticker_df = None, hist_df = None):

		self.ticker_df = ticker_df
		self.hist_df = hist_df

		if ticker_df is not None:
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