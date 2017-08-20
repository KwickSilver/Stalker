import boto3
from boto3.dynamodb.conditions import Key, Attr
import os

class StockDataDDB():
	def __init__(self):
		# Get the service resource.
		self.dynamodb = boto3.resource('dynamodb', region_name='ap-south-1', aws_access_key_id=os.environ['AWS_ACCESS_KEY'], aws_secret_access_key=os.environ['AWS_SECRET_KEY'])
		#self.dynamodb = boto3.resource('dynamodb', region_name='ap-south-1', aws_access_key_id='AKIAIUTLKCSEYCWGC55Q', aws_secret_access_key='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')
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



