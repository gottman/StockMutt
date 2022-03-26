
from datetime import datetime, timedelta

import cache_name
from cache_manager import CacheManager
from polygon_client import PolygonClient
from ticker_info import TickerInfo

class TickerData:

    DATE_KEY = 'date'
    CONTENT_KEY = 'content'
    SYMBOL_KEY = 'symbol'

    def __init__(self):
        self.client = PolygonClient()
        self.cache_manager = CacheManager(cache_name.TICKER_DATA)
        

    def get_ticker_data(self, days_of_history = 710, verbose = True):
        ticker_symbols = TickerInfo().get_ticker_symbol_list()
        ticker_data = self.cache_manager.read()

        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        day_to_process = today - timedelta(days=days_of_history)

        existing_dates = []
        if ticker_data:
            existing_dates = [datetime.fromisoformat(d) for d in ticker_data.keys()]
        else:
            ticker_data = {}
        while day_to_process < today:
            completed_symbols = []
            if day_to_process in existing_dates:
                completed_symbols = ticker_data[str(day_to_process)].keys()
            for symbol in ticker_symbols:
                if symbol not in completed_symbols:
                    if not str(day_to_process) in ticker_data.keys():
                        ticker_data[str(day_to_process)] = {}
                    ticker_data[str(day_to_process)][symbol] = self.client.load_ticker_data(symbol, day_to_process)
                    self.cache_manager.write(ticker_data)
            day_to_process = day_to_process + timedelta(days=1)