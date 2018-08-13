"""命令行火车票查看器
Usage:
    tickets [-gdtkz] <from> <to> <date>
"""
# Options:
#     -h,--help   显示帮助菜单
#     -g          高铁
#     -d          动车
#     -t          特快
#     -k          快速
#     -z          直达
# Example:
#       tickets 北京 上海 2016-10-10
#       python tickets.py 上海 北京 2018-08-02

from docopt import docopt
from parse_station import Stations
from InqueryTickets import InqueryTickets

arguments = docopt(__doc__)
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971'
station = Stations(url)
Inquery = InqueryTickets(station, arguments)
Inquery.inquery()
