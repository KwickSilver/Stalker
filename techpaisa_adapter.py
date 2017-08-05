import requests
from datetime import datetime,date
import json
from analyzer_constants import AnalyzerConstants
from ma_calculator import MACalculator

ma_calculator = MACalculator()
constants = AnalyzerConstants()
# Each API has hit limit of 100 hits/hour
#Visit API doc for more details: https://techpaisa.3scale.net/docs
#techpaisa_screen_api_url = 'http://techpaisa.com/api/stock-screener/?ind=nifty&app_id=92f8a520&app_key=85ce9c95989efc51c21678f5821e459f'
#response = requests.get(techpaisa_screen_api_url.format(app_id='your_app_id', app_key='your_app_key'))
date_format = "%Y/%m/%d"
techpaisa_analysis_api_url = 'http://techpaisa.com/api/chart/{nse_symbol}/{analysis_type}/?ind=nifty&app_id=92f8a520&app_key=85ce9c95989efc51c21678f5821e459f'
rsi = 'rsi'

class TPExtractor:
	def extract_stock_data(self, ticker, analysis_period):
		print "Extracting data for ticker: " + ticker
		rsi_json_data = self.get_data_list_from_json_response(ticker, rsi, analysis_period)

 		start_range = 0
 		# To handle the case when number of data is less than the analysis period and the first record will represent format.
 		rsi_json_data_length = len(rsi_json_data)
 		if rsi_json_data_length == 0:
 			return []

 		if rsi_json_data_length < analysis_period:
 			rsi_json_data.pop(0)

		rsi_json_data_length = len(rsi_json_data)

 		data = []
		# Extract date price and SMAs
		for index in range(start_range,rsi_json_data_length):
			one_day_data = rsi_json_data[index]
			print one_day_data
			print one_day_data[0]
			date = convert_json_date_to_string(one_day_data[0])
			data.append({constants.field_date:date, constants.field_price:float(one_day_data[1]), constants.field_rsi:float(one_day_data[2])}) 
		
		fill_moving_averages(data, rsi_json_data_length)
		return data


	def get_data_list_from_json_response(self, ticker, analysis_type, analysis_period):
		response = requests.get(techpaisa_analysis_api_url.format(nse_symbol=ticker, analysis_type=analysis_type, app_id='your_app_id', app_key='your_app_key'))
		#Convert string to JSON
		json_content = json.loads(response.content)
		if json_content['error'] == True:
			return []
		json_data = json_content['data']
		json_data = json_data[-1*analysis_period:]
		return json_data

def convert_json_date_to_string(json_date):
	datetime_object = datetime.strptime(json_date, date_format)
	date = datetime_object.strftime(date_format)
	return date

def fill_moving_averages(stock_data, length):
	ma_calculator.populate_n_day_ema_in_stock_data(5, stock_data, length, constants.field_ema_5, constants.field_price)
	ma_calculator.populate_n_day_ema_in_stock_data(10, stock_data, length, constants.field_ema_10, constants.field_price)
	ma_calculator.populate_n_day_ema_in_stock_data(20, stock_data, length, constants.field_ema_20, constants.field_price)

	ma_calculator.populate_n_day_sma_in_stock_data(20, stock_data, length, constants.field_sma_20, constants.field_price)
	ma_calculator.populate_n_day_sma_in_stock_data(50, stock_data, length, constants.field_sma_50, constants.field_price)
	ma_calculator.populate_n_day_sma_in_stock_data(100, stock_data, length, constants.field_sma_100, constants.field_price)
	ma_calculator.populate_n_day_sma_in_stock_data(200, stock_data, length, constants.field_sma_200, constants.field_price)
