import re
import requests


class Stations():
    """获取所有火车信息"""

    def __init__(self, url):
        self.url = url
        self.stations = []

    def get_stations(self):
        response = requests.get(self.url, verify=False)
        result = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
        self.stations = dict(result)
        return self.stations

    def get_key(self, value):
        """在字典里根据value查找key"""
        key = [k for k, v in self.stations.items() if v == value]
        return key[0]
