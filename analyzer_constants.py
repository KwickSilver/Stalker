from datetime import datetime,date

class AnalyzerConstants:
	stock_list_file_name = "stock_list"
	data_extraction_period = 700 # Prefer two years

	data_analysis_period = 30
	threshold_percentage = 60.00

	report_file = "report_file_" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	record_separator = "****************************\n"

	rsi_threshold = 50.00

	field_ticker = "ticker_name"
	field_ema_5 = "ema_5"
	field_ema_9 = "ema_9"
	field_ema_10 = "ema_10"
	field_ema_12 = "ema_12"
	field_ema_20 = "ema_20"
	field_ema_26 = "ema_26"
	field_ema_50 = "ema_50"
	
	field_rsi = "rsi"
	field_price = "price"
	field_date = "date"
	
	field_sma_200 = "sma_200"
	field_sma_100 = "sma_100"
	field_sma_50 = "sma_50"
	field_sma_20 = "sma_20"

	field_macd = "macd"
	field_macd_signal = "macd_signal"

	field_A = "field_A"
	field_B = "field_B"
	period = "period"
	percentage = "percentage"
	max_rsi = "max_rsi"
	comparer = "comparer"

	# Comparers
	over = "over"
	inside = "inside"

	# Percent range for inside comparer
	bracket = "bracket"
	
	def get_comparison_criterias(self):
		# add comparison criterias inside the constructor.
		comparison_criterias = []
		# define comparison criterias and add to self.comparison_criterias
		stock_climbing_up_from_sma_50 = []
		
		# INITIALIZE stock_climbing_up_from_sma_50
		stock_climbing_up_from_sma_50.append({self.comparer:self.over, self.field_A:self.field_price, self.field_B:self.field_sma_50, self.period:7, self.percentage:70.0, self.max_rsi: self.rsi_threshold})
		stock_climbing_up_from_sma_50.append({self.comparer:self.over, self.field_A:self.field_price, self.field_B:self.field_sma_20, self.period:10, self.percentage:70.0, self.max_rsi: self.rsi_threshold})
		stock_climbing_up_from_sma_50.append({self.comparer:self.over, self.field_A:self.field_price, self.field_B:self.field_ema_10, self.period:7, self.percentage:60.0, self.max_rsi: self.rsi_threshold})
		stock_climbing_up_from_sma_50.append({self.comparer:self.over, self.field_A:self.field_ema_5, self.field_B:self.field_sma_20, self.period:10, self.percentage:70.0, self.max_rsi: self.rsi_threshold})
		stock_climbing_up_from_sma_50.append({self.comparer:self.inside, self.bracket:20, self.field_A:self.field_price, self.field_B:self.field_sma_50, self.period:20, self.percentage:70.0, self.max_rsi: self.rsi_threshold})
		
		# just_bouncing_stock_from_200 = []
		# INITIALIZE just_bouncing_stock_from_200
		# self.just_bouncing_stock_from_200.append({self.comparer:self.over, self.field_A:self.field_price, self.field_B:self.field_sma_200, self.period:10, self.percentage:70.0, self.max_rsi: self.rsi_threshold})
		# self.just_bouncing_stock_from_200.append({self.comparer:self.over, self.field_A:self.field_price, self.field_B:self.field_sma_50, self.period:10, self.percentage:70.0, self.max_rsi: self.rsi_threshold})
		# self.just_bouncing_stock_from_200.append({self.comparer:self.over, self.field_A:self.field_price, self.field_B:self.field_sma_20, self.period:10, self.percentage:70.0, self.max_rsi: self.rsi_threshold})
		# self.just_bouncing_stock_from_200.append({self.comparer:self.over, self.field_A:self.field_price, self.field_B:self.field_ema_10, self.period:7, self.percentage:60.0, self.max_rsi: self.rsi_threshold})
		# self.just_bouncing_stock_from_200.append({self.comparer:self.over, self.field_A:self.field_ema_5, self.field_B:self.field_sma_20, self.period:10, self.percentage:70.0, self.max_rsi: self.rsi_threshold})
		
		comparison_criterias.append(stock_climbing_up_from_sma_50)
		return comparison_criterias
