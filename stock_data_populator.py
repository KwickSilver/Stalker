from stock_data_ddb import StockDataDDB
from ticker_ddb import TickerDDB
from techpaisa_adapter import TPExtractor
from error_sqs_adapter import ErrorSQS
from datetime import datetime
from progressbar import Bar, ETA, Percentage, ProgressBar, Timer

widgets = [Percentage(), ' ', Bar(), ' ', ETA()]
pbar = ProgressBar(widgets=widgets, maxval=500)

stock_ddb_accessor = StockDataDDB()
ticker_ddb_accessor = TickerDDB()
tp_extractor = TPExtractor()
error_sqs = ErrorSQS()

tickers = ticker_ddb_accessor.get_batch()

for ticker in pbar(tickers):
	ticker_name = ticker['ticker_name']
	current_date = datetime.today()
	last_date = stock_ddb_accessor.get_last_date(ticker_name)
	if last_date is None:
		analysis_period = 2500
	else:
		analysis_period = (current_date - last_date).days - 1
	try:
		if analysis_period > 0 :
			#print "STOCK_DATA_POPULATOR: populating data for ticker: " + ticker_name
			#print "STOCK_DATA_POPULATOR: Analysis period: " + str(analysis_period)
			stock_data = tp_extractor.extract_stock_data(ticker_name, analysis_period)
			#print "STOCK_DATA_POPULATOR: Writing data to stock_data_ddb"
			stock_ddb_accessor.batch_put(stock_data)
			#print "STOCK_DATA_POPULATOR: Completed writing data to stock_data_ddb"
	except KeyboardInterrupt:
		print "\n\nQuitting stock data population ...\n"
		print "bye ...\n"
		break
	except Exception as error:
		#print "STOCK_DATA_POPULATOR: An error occurred while processing the ticker: " + ticker_name
		error_sqs.send_error_message(ticker_name, current_date.strftime('%Y-%m-%d'), analysis_period, error)
		continue