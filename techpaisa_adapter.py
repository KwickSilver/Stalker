import requests
from datetime import datetime,date
import json
from analyzer_constants import AnalyzerConstants

constants = AnalyzerConstants()
# Each API has hit limit of 100 hits/hour
#Visit API doc for more details: https://techpaisa.3scale.net/docs
#techpaisa_screen_api_url = 'http://techpaisa.com/api/stock-screener/?ind=nifty&app_id=92f8a520&app_key=85ce9c95989efc51c21678f5821e459f'
#response = requests.get(techpaisa_screen_api_url.format(app_id='your_app_id', app_key='your_app_key'))
date_format = "%Y/%m/%d"
techpaisa_analysis_api_url = 'http://techpaisa.com/api/chart/{nse_symbol}/{analysis_type}/?ind=nifty&app_id=92f8a520&app_key=85ce9c95989efc51c21678f5821e459f'
sma = 'sma'
rsi = 'rsi'

class TPExtractor:
	def extract_stock_data(self, ticker, analysis_period):
		print "Extracting data for ticker: " + ticker
		sma_json_data = self.get_data_list_from_json_response(ticker, sma, analysis_period)
		rsi_json_data = self.get_data_list_from_json_response(ticker, rsi, analysis_period)

 		start_range = 0
 		# To handle the case when number of data is less than the analysis period and the first record will represent format.
 		sma_data_length = len(sma_json_data)
 		if sma_data_length == 0:
 			return []

 		if sma_data_length < analysis_period:
 			sma_json_data.pop(0)
 			rsi_json_data.pop(0)

		sma_data_length = len(sma_json_data)
		rsi_data_length = len(rsi_json_data)

 		data = []
		# Extract date price and SMAs
		for index in range(start_range,sma_data_length):
			stock_json = sma_json_data[index]
			date = convert_json_date_to_string(stock_json[0])
			data.append({"date":date, "price":float(stock_json[1]), constants.field_sma_20:float(stock_json[2]), constants.field_sma_50:float(stock_json[3]), constants.field_sma_200:float(stock_json[4])})

		# Extract RSIs
		if sma_data_length == rsi_data_length:
			for index in range(start_range,sma_data_length):
				# Confirming that the RSI is of the same date as the Price and SMAs
				if convert_json_date_to_string(rsi_json_data[index][0]) == data[index]['date']:
					data[index]['rsi'] = float(rsi_json_data[index][2])
		else: 
			print "Not including RSIs"
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
