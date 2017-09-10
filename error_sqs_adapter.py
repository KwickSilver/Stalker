import boto3
import os
import pandas

class ErrorSQS():
	def __init__(self):
		
		accessKeys = pandas.read_csv('accessKeys.csv')
		access_key_id = accessKeys['Access key ID'][0]
		secret_access_key = accessKeys['Secret access key'][0]
		
		# Get the service resource.
		self.sqs = boto3.resource('sqs', region_name='ap-south-1', aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)
		
		# Get the queue. This returns an SQS.Queue instance
		self.queue = self.sqs.get_queue_by_name(QueueName='stock_data_populator_error')

	def send_error_message(self, ticker_name, date, analysis_period, error):
		self.queue.send_message(MessageBody='error', MessageAttributes={
			'ticker_name': {
			    'StringValue': ticker_name,
			    'DataType': 'String'
			},
			'date': {
			    'StringValue': date,
			    'DataType': 'String'
			},
			'analysis_period': {
			    'StringValue': str(analysis_period),
			    'DataType': 'Number'
			},
			'error': {
			    'StringValue': str(error),
			    'DataType': 'String'
			}

		})