from analyzer_constants import AnalyzerConstants
from decimal import Decimal
import math

constants = AnalyzerConstants()

class MACalculator:

	def populate_n_day_ema_in_stock_data(self, period, stock_data, length, ema_field, price_field):
		
		multiplier = (2 / Decimal(1 + period))
		stock_data[0][ema_field] = stock_data[0][price_field]
		for index in range(1, length):
			current_price = stock_data[index][price_field]
			prev_ema = stock_data[index - 1][ema_field]
			stock_data[index][ema_field] = round_off((current_price - prev_ema) * multiplier + prev_ema, 2)

	def populate_n_day_sma_in_stock_data(self, period, stock_data, length, field_name, field_price):

		stock_data[0][field_name] = stock_data[0][field_price]
		sum = stock_data[0][field_price]
		
		period = min(period, length)
		for index in range(1, period):
			sum = sum + stock_data[index][field_price]
			stock_data[index][field_name] = round_off(sum / (index+1), 2)

		for index in range(period, length):
			sum = sum - stock_data[index - period][field_price]
			sum = sum + stock_data[index][field_price]
			stock_data[index][field_name] = round_off(sum / period, 2)

	def populate_macd_in_stock_data(self, stock_data, length, field_macd, field_signal):

		# For MACD calculation
		self.populate_n_day_ema_in_stock_data(12, stock_data, length, constants.field_ema_12, constants.field_price)
		self.populate_n_day_ema_in_stock_data(26, stock_data, length, constants.field_ema_26, constants.field_price)

		for index in range(0, length):
			stock_data[index][field_macd] = stock_data[index][constants.field_ema_12] - stock_data[index][constants.field_ema_26]

		self.populate_n_day_ema_in_stock_data(9, stock_data, length, field_signal, field_macd)

		for index in range(0, length):
			stock_data[index].pop(constants.field_ema_12)
			stock_data[index].pop(constants.field_ema_26)

def round_off(number, places):
	number = round(number, places)
	return Decimal(str(number))