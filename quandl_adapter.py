import quandl

class QuandlAdapter:
	def __init__(self):
		quandl.ApiConfig.api_key = "xx89auVCwzDdPg7C6pZ2"

	def get_stock_history(self, ticker, start, end):
		return quandl.get("NSE/" + ticker, start_date=start.strftime('%d-%m-%Y'), end_date=end.strftime('%d-%m-%Y'))

	def get_complete_stock_history(self, ticker):
		return quandl.get("NSE/" + ticker)