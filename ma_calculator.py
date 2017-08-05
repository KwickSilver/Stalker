
class MACalculator:

	def populate_n_day_ema_in_stock_data(self, period, stock_data, length, ema_field, price_field):
		
		multiplier = 2 / float(1 + period)
		# as we dont know the n day sma for stock_data[0], asuming it as stock_data[0][price_field]
		stock_data[0][ema_field] = stock_data[0][price_field]
		for index in range(1, length):
			current_values = stock_data[index]
			prev_values = stock_data[index - 1]
			stock_data[index][ema_field] = (current_values[price_field] - prev_values[ema_field]) * multiplier + prev_values[ema_field]

	def populate_n_day_sma_in_stock_data(self, period, stock_data, length, field_name, field_price):

		stock_data[0][field_name] = stock_data[0][field_price]
		sum = stock_data[0][field_price]
		
		for index in range(1, period):
			sum = sum + stock_data[index][field_price]
			stock_data[index][field_name] = sum / (index+1)

		for index in range(period, length):
			sum = sum - stock_data[index - period][field_price]
			sum = sum + stock_data[index][field_price]
			stock_data[index][field_name] = sum / period