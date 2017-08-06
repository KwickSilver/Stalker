import boto3
from boto3.dynamodb.conditions import Key, Attr

class StockDataDDB():
	def __init__(self):
		# Get the service resource.
		self.dynamodb = boto3.resource('dynamodb', region_name='ap-south-1', aws_access_key_id='AKIAJQV3HABYI5WIIFJA',aws_secret_access_key='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')
		self.table = self.dynamodb.Table('stock_data')

	def put(self, stock_data):
		self.table.put_item(Item = self.get_item(stock_data))

	def batch_put(self, stock_data):
		with self.table.batch_writer() as batch:
			for data in stock_data:
				batch.put_item(Item = self.get_item(data))

	def get(self, ticker_name):
		response = self.table.query(KeyConditionExpression=Key('ticker_name').eq(ticker_name))
		#print response['Items']
		return response['Items']

	def get(self, ticker_name, date):
		response = self.table.query(
			KeyConditionExpression=Key('ticker_name').eq(ticker_name) & Key('date').eq(date))
		#print response['Items']
		return response['Items']

	def batch_get(self):
		response = self.table.scan()
		#print response['Items']
		return response['Items']

	def get_item(self, stock_data):
		item = {}
		for key, value in stock_data.items():
				item[key] = value

		return item;



