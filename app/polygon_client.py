import config
import requests
import time
from datetime import datetime, timedelta

import cache_name
from access_limit_util import AccessLimitUtil

class PolygonClient:
    
    def __init__(self, error_attempts = 5, error_wait = 5):
        self.error_attempts = error_attempts
        self.error_wait = error_wait

    def load_ticker_info(self,  limit = 5, limit_wait = 5):

        access_limiter = AccessLimitUtil(cache_name.POLYGON_ACCESS_LIMIT, limit, timedelta(seconds=60))
        url = config.POLYGON_IO_TICKERS_ENDPOINT
        result = []

        while url:
            if not access_limiter.is_limited():
                response = requests.get(url, {
                    'apiKey': config.POLYGON_IO_REST_API_KEY,
                    'type': 'CS',
                    'market': 'stocks',
                    'limit': 1000
                }).json()
                result.extend(response["results"])
                access_limiter.log_access()
                if 'next_url' in response.keys():
                    url = response['next_url']
                else:
                    url = None
            else:
                print("Polygon access limit reached! Waiting 5")
                time.sleep(limit_wait)
        return result

    def load_ticker_data(self, ticker_symbol, date, limit = 5, limit_wait = 5, verbose = True):
        
        access_limiter = AccessLimitUtil(cache_name.POLYGON_ACCESS_LIMIT, limit, timedelta(seconds=60))
        date_string = date.strftime("%Y-%m-%d")
        url = "/".join([config.POLYGON_IO_OPEN_CLOSE_ENDPOINT, ticker_symbol, date_string])
        result = None
        while url:
            if not access_limiter.is_limited():
                try:
                    response = requests.get(url, {
                        'apiKey': config.POLYGON_IO_REST_API_KEY,
                        'stocksTicker': ticker_symbol,
                        'date': date_string,
                        'adjusted': True
                    }).json()  
                    access_limiter.log_access()
                    if response['status'] == "OK":
                        result = response
                    if verbose:
                        print(f"{{ ticker: {ticker_symbol}, response: {response['status']} }}")
                    url = None
                except ConnectionError:
                    time.sleep(180)
            else:
                print("Polygon access limit reached! Waiting...")
                time.sleep(limit_wait)
        return result