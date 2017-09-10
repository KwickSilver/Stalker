from stock_data_ddb import StockDataDDB
from ticker_ddb import TickerDDB
from techpaisa_adapter import TPExtractor
from datetime import datetime

stock_ddb_accessor = StockDataDDB()
ticker_ddb_accessor = TickerDDB()
tp_extractor = TPExtractor()

tickers = ticker_ddb_accessor.get_batch()

for ticker in tickers:
	try:
		analysis_period = (datetime.now() - stock_ddb_accessor.get_last_date(ticker)).days
		stock_data = tp_extractor.extract_stock_data(ticker, analysis_period)

		print "STOCK_DATA_POPULATOR: Analysis period: " + str(analysis_period)
		print "STOCK_DATA_POPULATOR: Writing data to stock_data_ddb"
		stock_ddb_accessor.batch_put(stock_data)
		print "STOCK_DATA_POPULATOR: Completed writing data to stock_data_ddb"
	except:
		print "STOCK_DATA_POPULATOR: An error occurred while processing the ticker: " + ticker_name
		continue