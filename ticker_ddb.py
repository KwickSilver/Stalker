import boto3
import os

class TickerDDB():
	def __init__(self):
		# Get the service resource.
		self.dynamodb = boto3.resource('dynamodb', region_name='ap-south-1', aws_access_key_id=os.environ['AWS_ACCESS_KEY'],aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
		self.table = self.dynamodb.Table('ticker')

	def put(self, ticker_name, ticker_description):
		self.table.put_item(
			Item={
			'ticker_name': ticker_name,
			'ticker_description': ticker_description
			})

	def batch_batch(self, tickers):
		with self.table.batch_writer() as batch:
			for ticker_name,ticker_description in tickers.items():
				batch.put_item(
					Item={
					'ticker_name': ticker_name.decode('unicode_escape').encode('utf-8'),
					'ticker_description': ticker_description.decode('unicode_escape').encode('utf-8')
					})

	def get_batch(self):
		response = self.table.scan()
		items = response['Items']
		return items

