from datetime import datetime
from cache_manager import CacheManager

class AccessLimitUtil:
    access_log_key = 'access_log'

    def __init__(self, filename, limit, timedelta):
        self.filename = filename
        self.limit = limit
        self.timedelta = timedelta
        self.cache_manager = CacheManager(filename)

    def log_access(self):
        data = self.cache_manager.read()
        if data and data[self.access_log_key]:
            data[self.access_log_key].append(datetime.now())
            self.cache_manager.write(data)
        else:
            new_data = {}
            new_data[self.access_log_key] = [datetime.now()]
            self.cache_manager.write(new_data)

    def is_limited(self):
        data = self.cache_manager.read()
        updated_data = {}
        updated_data[self.access_log_key] = []
        if data and data[self.access_log_key]:
            hits = 0
            left_gate = datetime.now() - self.timedelta
            for logged_access_string in data[self.access_log_key]:
                logged_access = datetime.fromisoformat(logged_access_string)
                if logged_access >= left_gate:
                    hits+=1
                    updated_data[self.access_log_key].append(logged_access)
            self.cache_manager.write(updated_data)
            return hits > self.limit - 1
        else:
            return False