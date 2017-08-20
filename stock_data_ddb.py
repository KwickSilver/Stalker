import boto3
import datetime
import pandas as pd
from boto3.dynamodb.conditions import Key, Attr
import os

class StockDataDDB():
	def __init__(self):
		# Get the service resource.

		accessKeys = pd.read_csv('accessKeys.csv')
		access_key_id = accessKeys['Access key ID'][0]
		secret_access_key = accessKeys['Secret access key'][0]
		self.dynamodb = boto3.resource('dynamodb', region_name='ap-south-1', aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key)
		self.table = self.dynamodb.Table('stock_data')

	def put(self, stock_data):
		self.table.put_item(Item = self.get_item(stock_data))

	def batch_put(self, stock_data):
		with self.table.batch_writer() as batch:
			for data in stock_data:
				batch.put_item(Item = self.get_item(data))

	def get(self, ticker_name, start_date=None, end_date=None):
		if start_date is None:
			response = self.table.query(KeyConditionExpression=Key('ticker_name').eq(ticker_name));
		else:
			if end_date is None:
				end_date = start_date
			date1 = long(start_date.strftime("%Y%m%d"))
			date2 = long(end_date.strftime("%Y%m%d"))
			response = self.table.query(KeyConditionExpression=Key('ticker_name').eq(ticker_name) & Key('date').between(date1, date2))
		return response['Items']

	def get_last_n_data(self, ticker_name, n=None):
		if n is None:
			response = self.table.query(KeyConditionExpression=Key('ticker_name').eq(ticker_name));
		else:
			response = self.table.query(KeyConditionExpression=Key('ticker_name').eq(ticker_name), ScanIndexForward=False, Limit=n)
		return response['Items']

	def get_first_date(self, ticker_name):
		response = self.table.query(KeyConditionExpression=Key('ticker_name').eq(ticker_name), ScanIndexForward=False, Limit=1)
		if len(response['Items']) > 0:
			return response['Items'][0].get('date')
		else:
			return None;
	
	def get_last_date(self, ticker_name):
		response = self.table.query(KeyConditionExpression=Key('ticker_name').eq(ticker_name), ScanIndexForward=True, Limit=1)
		if len(response['Items']) > 0:
			return response['Items'][0].get('date')
		else:
			return None;

	def batch_get(self):
		response = self.table.scan()
		#print response['Items']
		return response['Items']

	def get_item(self, stock_data):
		item = {}
		for key, value in stock_data.items():
				item[key] = value
		return item;



