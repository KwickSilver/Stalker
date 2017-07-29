from rtstock.stock import Stock
from rtstock.utils import download_historical
from rtstock.utils import request_historical
# Realtime stocks documentation: https://realtime-stock.readthedocs.io/en/latest/

class RealTimeStockAdapter:
	'Adapter for RealTimeStock'
	__default_ticker = 'AMZN';

	def __init__(self):
		self.stock = Stock('')

	def get_info(self, ticker):
		self.stock.set_ticker(ticker)
		return self.stock.get_info()

	def get_latest_price(self, ticker):
		self.stock.set_ticker(ticker)
		return self.stock.get_latest_price()[0].get('LastTradePriceOnly')

	def get_historical(self, ticker, start_date, end_date):
		self.stock.set_ticker(ticker)
		print self.stock.get_ticker() + '#'
		return self.stock.get_historical(start_date, end_date)

	def save_historical(self, ticker, output_folder):
		self.stock.set_ticker(ticker)
		self.stock.save_historical(output_folder)

	def download_historical(self, tickers_list, output_folder):
		download_historical(tickers_list, output_folder)

	def request_historical(self, ticker, start_date, end_date):
		return request_historical(ticker, start_date, end_date)
