from nsetools import Nse

#nse-tools usage: http://nsetools.readthedocs.io/en/latest/usage.html
class NSEAdapter:
	'Adapter for NSE'
	def __init__(self):
		self.__nse = Nse()

	def get_all_stock_codes(self):
		return self.__nse.get_stock_codes()
	
	def get_current_stock_price(self, tinker):
		return self.__nse.get_quote(tinker)

	def get_top_gainers(self):
		top_gainers_name = list()
		for top_gainers in self.__nse.get_top_gainers():
			top_gainers_name.append(top_gainers.get('symbol'))
		return top_gainers_name

	def get_top_losers(self):
		top_losers_name = list()
		for top_losers in self.__nse.get_top_losers():
			top_losers_name.append(top_losers.get('symbol'))
		return top_losers_name