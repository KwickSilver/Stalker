from techpaisa_adapter import TPExtractor
from ema_calculator import EMACalculator

from time import time
from stock_analyzer_helper import StockAnalyzerHelper
from analyzer_constants import AnalyzerConstants

tp_ext = TPExtractor()
ema_calc = EMACalculator()
helper = StockAnalyzerHelper()
constants = AnalyzerConstants()

comparison_criterias = constants.get_comparison_criterias()

def extract_stock_names_from_file(file_name):
	with open(file_name) as file:
	    all_stocks = file.readlines()
		# Remove whitespace characters like `\n` at the end of each line
	all_stocks = [x.strip() for x in all_stocks]
	return all_stocks

def append_to_report_file(file_name, text):
	with open(file_name, "a") as report:
		report.write(text)
		#report.write(constants.record_separator)

def fill_10_and_5_day_emas():
	ema_calc.populate_n_day_ema_in_stock_data(10, stock_data, constants.field_ema_10, constants.field_sma_20, constants.field_price)
	ema_calc.populate_n_day_ema_in_stock_data(5, stock_data, constants.field_ema_5, constants.field_sma_20, constants.field_price)

def analyze(stock_data, length, stock_criterias):
	results = []
	for criteria in stock_criterias:
		if criteria[constants.comparer] == constants.over:
			results.append(helper.is_A_over_B_for_x_percent_times_in_last_n_days(stock_data, criteria[constants.field_A], criteria[constants.field_B], criteria[constants.period], criteria[constants.percentage]))
		elif criteria[constants.comparer] == constants.inside:
			results.append(helper.is_A_inside_B_for_bracket_range_for_x_percent_times_in_last_n_days(stock_data, criteria[constants.field_A], criteria[constants.field_B], criteria[constants.period], criteria[constants.percentage], criteria[constants.bracket]))
	return results

def add_result_to_report(ticker, stock_criterias, results, stock_data, length):
	for result in results:
		if result == False:
			return
	report_string = ticker + '\n'
	#for criteria in stock_criterias:
	#	report_string += str(criteria[constants.field_A]) + " " + str(criteria[constants.comparer]) + " " + str(criteria[constants.field_B]) + " for period = " + str(criteria[constants.period]) + " days and percentage times = " + str(criteria[constants.percentage]) + " Rsi threshold = " + str(criteria[constants.max_rsi]) + "\n"
	#report_string += str(stock_data[length-1]) + "\n"
	append_to_report_file(constants.report_file, report_string)


all_tickers = extract_stock_names_from_file(constants.stock_list_file_name)
for ticker in all_tickers:
	start_time = time()
	stock_data = tp_ext.extract_stock_data(ticker, constants.data_extraction_period)
	length = len(stock_data)
	# Stock data does not exist
	if length == 0:
		print "No data found for ticker = " + ticker
		continue

	# Fill 10 day and 5 day EMA values in our stock_data
	fill_10_and_5_day_emas()

	for criteria in comparison_criterias:
		results = analyze(stock_data, length, criteria)
		add_result_to_report(ticker, criteria, results, stock_data, length)

	end_time = time()
	total_processing_time = end_time - start_time
	#print "Processing Time: " + str(total_processing_time)
	append_to_report_file("active_stocks", ticker+"\n")
