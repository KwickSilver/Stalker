
class EMACalculator:

	def populate_n_day_ema_in_stock_data(self, period, stock_data, ema_field, sma_field, price_field):
		multiplier = 2 / float(1 + period)
		# as we dont know the n day sma for stock_data[0], asuming it as stock_data[0][sma_field]
		stock_data[0][ema_field] = stock_data[0][sma_field]
		for index in range(1,len(stock_data)):
			current_values = stock_data[index]
			prev_values = stock_data[index - 1]
			stock_data[index][ema_field] = (current_values[price_field] - prev_values[ema_field]) * multiplier + prev_values[ema_field]
