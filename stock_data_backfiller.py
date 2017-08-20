from stock_data_ddb import StockDataDDB
from ticker_ddb import TickerDDB
from techpaisa_adapter import TPExtractor
from decimal import Decimal
from time import time, sleep


def extract_stock_names_from_file(file_name):
	with open(file_name) as file:
	    all_stocks = file.readlines()
		# Remove whitespace characters like `\n` at the end of each line
	all_stocks = [x.strip() for x in all_stocks]
	return all_stocks

def add_to_errored_stocks(ticker):
	with open("errored_stocks", "a") as report:
		report.write(ticker + '\n')
ddb_stock_data_accessor = StockDataDDB()
ddb_all_ticker_accessor = TickerDDB()
tp_extractor = TPExtractor()

analysis_period = 2500 # 10 year data

#all_stock_tickers = ddb_all_ticker_accessor.get_batch()
all_stock_tickers = extract_stock_names_from_file("stock_list")
number_of_tickers = len(all_stock_tickers)

print "Total Number of stock tickers: " + str(number_of_tickers)

start_time = time()
for index in range(0, number_of_tickers):
	ticker_name = all_stock_tickers[index]#['ticker_name']
	print str(index+1) + ". " + str(ticker_name)
	try:
		stock_data = tp_extractor.extract_stock_data(ticker_name, analysis_period)
		print "Writing data to ddb"
		ddb_stock_data_accessor.batch_put(stock_data)
		print "Completed Writing data to ddb"
	except:
		print "AN ERROR OCCURED WHILE PROCESSING THE TICKER: " + ticker_name
		add_to_errored_stocks(ticker_name)
		continue
	#sleep(3) # to avoid exceeding the provisioned throughput and perform retries on throttled requests

end_time = time()

print "Total Time: " + str(end_time - start_time)

