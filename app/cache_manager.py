from functools import cache
from genericpath import isdir
import json
import time
import os

class CacheManager:
    cache_folder = "local_cache"
    cache_extension = ".json"

    def __init__(self, filename):
        if not os.path.isdir(self.cache_folder):
            os.mkdir(self.cache_folder)
        self.save_location = "".join([os.path.join(self.cache_folder, filename), self.cache_extension])
        self.locked = False

    def write(self, data):
        while self.locked:
            print("Waiting for lock to resolve")
            time.sleep(1)
        self.locked = True
        with open(self.save_location, 'w+') as f:
            json.dump(data, f, indent=4, sort_keys=True, default=str)
        self.locked = False

    def read(self):
        while self.locked:
            print("Waiting for lock to resolve")
            time.sleep(1)
        try:
            self.locked = True
            f = open(self.save_location, 'r')
            data = json.load(f)
            self.locked = False
            f.close()
            return data
        except FileNotFoundError:
            self.locked = False
            return None