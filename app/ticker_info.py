import cache_name

from datetime import datetime, timedelta

from cache_manager import CacheManager
from polygon_client import PolygonClient

class TickerInfo:

    last_updated_key = "last_updated"
    content_key = "content"

    def __init__(self):
        self.cache_manager = CacheManager(cache_name.TICKER_INFO)


    def get_ticker_info(self, refresh_older_than = timedelta(days = 30)):
        ticker_info = self.cache_manager.read()
        if ticker_info and ticker_info[self.last_updated_key]:
            if((datetime.now() - refresh_older_than) > datetime.fromisoformat(ticker_info[self.last_updated_key])):
                return self.fetch_ticker_info()
            else:
                return ticker_info
        else:
            return self.fetch_ticker_info()
        
        
    def get_ticker_symbol_list(self):
        result = []
        ticker_info = self.get_ticker_info()
        if ticker_info[self.content_key]:
            for content in ticker_info[self.content_key]:
                if content["ticker"]:
                    result.append(content["ticker"])
        return result


    def fetch_ticker_info(self):
        client = PolygonClient()
        data = {}
        data[self.content_key] = client.load_ticker_info()
        data[self.last_updated_key] = datetime.now()
        self.cache_manager.write(data)
        return data