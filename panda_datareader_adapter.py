import datetime as dt
import pandas_datareader.data as web
from rtstock.stock import Stock
from nsetools import Nse

# pandas-datareader usage: http://pandas-datareader.readthedocs.io/en/latest/remote_data.html

class PandasDataReaderAdapter:
	'Class to fetch stock related data from available remote servers' 

	# list of available remote data source.
	__available_data_source = set(['google', 'yahoo'])

	# default remote data source.
	__default_data_source = 'google'

	def __init__(self, data_source):
		# defaults to 'google' if remote_server is invalid
		if data_source in self.__available_data_source:
			self.data_source = data_source
		else:
			self.data_source = self.__default_data_source

	# API to get stock data between start_date and end_date.
	# returns:  dataFrame
	def get_stock_data(self, ticker, start_date, end_date):
		return web.DataReader(ticker, self.data_source, start_date, end_date)