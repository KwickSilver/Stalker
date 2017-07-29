from nsepy import get_history, get_index_pe_history
import datetime as dt

class NSEPyAdapter:
	'Adapter for NSEPy'
	pass
	
	def get_stock_history(self, ticker, start, end):
		return get_history(ticker, start, end)

#print get_stock_history('SBIN', dt.datetime(2017, 7, 1), dt.datetime.now())