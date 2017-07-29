from panda_datareader_adapter import PandasDataReaderAdapter
from realtime_stock_adapter import RealTimeStockAdapter
from nse_adapter import NSEAdapter
from nse_scrapper import NSEScrapper
from quandl_adapter import QuandlAdapter
import datetime as dt
from dateutil import relativedelta
import re
import time

ft = PandasDataReaderAdapter('google')
nse = NSEAdapter()
quandl = QuandlAdapter()
rsa = RealTimeStockAdapter()
nse_scr = NSEScrapper()
nse_ticker_pattern = re.compile("NSE:[A-Z]+")

def get_stock_price_n_days_back(ticker, n):
	if (n<=1):
		if (is_nse_ticker(ticker)) :
			return nse.get_current_stock_price(ticker[4:]).get('lastPrice')
		else :
			return rsa.get_latest_price(ticker)
	else:
		current_time = dt.datetime.now()
		time_n_days_back = current_time - relativedelta.relativedelta(days=n)
		return get_stock_price(ticker, time_n_days_back, current_time)



def get_stock_price_n_months_back(ticker, n):
	current_time = dt.datetime.now()
	time_n_months_back = current_time - relativedelta.relativedelta(months=n)
	return get_stock_price(ticker, time_n_months_back, current_time)


def get_stock_price_n_years_back(ticker, n):
	current_time = dt.datetime.now()
	time_n_years_back = current_time - relativedelta.relativedelta(years=n)
	return get_stock_price(ticker, time_n_years_back, current_time)

def get_stock_price(ticker, start, end):
	if (is_nse_ticker(ticker)):
		return get_nse_stock_price(ticker[4:], start, end)
	else :
		return get_non_nse_stock_price(ticker, start, end)

def get_nse_stock_price(ticker, start, end):
	return quandl.get_stock_history(ticker, start, end).head(1).iloc[0]['Close']

def get_non_nse_stock_price(ticker, start, end):
	return ft.get_stock_data(ticker, start, end).head(1).iloc[0]['Close']

def is_nse_ticker(ticker):
	return nse_ticker_pattern.match(ticker)

def get_stock_price_for_all_nse_stocks():
	stock_codes = nse.get_all_stock_codes()
	count = 0;
	print dt.datetime.now()
	for stock_code in stock_codes:
		count += 1;
		try:
			print count, '.', stock_code, " : ", get_stock_price_n_days_back('NSE:' + stock_code, 5)
		except Exception:
			print 'OOPS!!, got an exception'

		 

	print dt.datetime.now()

#get_stock_price_for_all_nse_stocks()
#print get_stock_price_n_days_back('NSE:HDFCBANK', 1)

start = dt.datetime.now() - relativedelta.relativedelta(days=50)
end = dt.datetime.now()
print quandl.get_stock_history('HDFCBANK', start, end)
print ft.get_stock_data('AMZN', start, end)
print nse.get_top_gainers()
print nse.get_top_losers()
#print get_stock_price_n_months_back('NSE:HDFCBANK', 1)

#print get_stock_price_n_years_back('NSE:HDFCBANK', 5)

#print get_stock_price_n_years_back('KO', 10)

#print rsa.get_latest_price('NSE:HDFC')

