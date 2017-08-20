import boto3
import os

class TickerDDB():
	def __init__(self):
		# Get the service resource.
		accessKeys = pd.read_csv('accessKeys.csv')
		access_key_id = accessKeys['Access key ID'][0]
		secret_access_key = accessKeys['Secret access key'][0]
		self.dynamodb = boto3.resource('dynamodb', region_name='ap-south-1', aws_access_key_id='AKIAJQV3HABYI5WIIFJA',aws_secret_access_key='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')
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

