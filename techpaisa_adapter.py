import requests
import pandas as pd
import io

# Each API has hit limit of 100 hits/hour
#Visit API doc for more details: https://techpaisa.3scale.net/docs
techpaisa_screen_api_url = 'http://techpaisa.com/api/stock-screener/?ind=nifty&app_id={app_id}&app_key={app_key}'
techpaisa_analysis_api_url = 'http://techpaisa.com/api/chart/{nse_symbol}/{analysis_type}/?ind=nifty&app_id={app_id}&app_key={app_key}'

#response = requests.get(techpaisa_screen_api_url.format(app_id='your_app_id', app_key='your_app_key'))

#response = requests.get(techpaisa_analysis_api_url.format(nse_symbol='HDFCBANK', analysis_type='sma', app_id='your_app_id', app_key='your_app_key'))
#data = response.content
#print data
