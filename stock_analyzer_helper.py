
class StockAnalyzerHelper:

	def is_A_over_B_for_x_percent_times_in_last_n_days(self, stock_data, field_A, field_B, n, x_percent):
		
		# Last n day or less data
		last_n_day_data = stock_data[-1*n:]
		number_of_samples = len(last_n_day_data)
		difference_A_B = []

		for one_day_data in last_n_day_data:
			difference_A_B.append({"diff":one_day_data[field_A] - one_day_data[field_B]})

		# Calculating at every point number of positives and negatives on its right
		# including this sample to see if there was a cross over.
		difference_A_B[number_of_samples-1]["right_pos"] = 0
		difference_A_B[number_of_samples-1]["right_neg"] = 0

		if difference_A_B[number_of_samples-1]["diff"] >= 0:
			difference_A_B[number_of_samples-1]["right_pos"] = 1
		else:
			difference_A_B[number_of_samples-1]["right_neg"] = 1
		
		for index in range(number_of_samples - 2, -1, -1):
			difference_A_B[index]["right_pos"] = difference_A_B[index+1]["right_pos"]
			difference_A_B[index]["right_neg"] = difference_A_B[index+1]["right_neg"]
			if difference_A_B[index]["diff"] >= 0:
				difference_A_B[index]["right_pos"] = difference_A_B[index]["right_pos"] + 1
			else:
				difference_A_B[index]["right_neg"] = difference_A_B[index]["right_neg"] + 1

		required_number = number_of_samples * x_percent / 100.0 # X% of the number of samples
		for value in difference_A_B:
			difference_pos_neg = value["right_pos"] - value["right_neg"]
			if difference_pos_neg >= required_number:
				return True
		return False

	def is_A_inside_B_for_bracket_range_for_x_percent_times_in_last_n_days(self, stock_data, field_A, field_B, n, x_percent, bracket):
		last_n_day_data = stock_data[-1*n:]
		number_of_samples = len(last_n_day_data)

		counter = 0
		for one_day_data in last_n_day_data:
			difference = one_day_data[field_A] - one_day_data[field_B]
			if ( (100.00 * abs(difference))/one_day_data[field_B] <= bracket):
				counter = counter + 1
		if counter >= number_of_samples * x_percent / 100.0:
			return True
		return False
