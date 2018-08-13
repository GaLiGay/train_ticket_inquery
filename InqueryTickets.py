import requests
import warnings
from prettytable import PrettyTable


class InqueryTickets():
    """查询票价"""

    def __init__(self, _station, arguments):
        self.arguments = arguments
        self.station = _station
        self.stations = self.station.get_stations()
        self.table = PrettyTable()
        self.train_number = None
        self.from_station_code = None
        self.to_station_code = None
        self.start_time = None
        self.arrive_time = None
        self.time_duration = None
        self.first_class_seat = None
        self.second_class_seat = None
        self.soft_sleep = None
        self.hard_sleep = None
        self.hard_seat = None
        self.no_seat = None

    def inquery(self):
        from_station = self.stations.get(self.arguments['<from>'])
        to_station = self.stations.get(self.arguments['<to>'])
        date = self.arguments['<date>']
        options = ''.join([key for key, value in self.arguments.items() if value is True])
        url = 'https://kyfw.12306.cn/otn/leftTicket/query?' \
              'leftTicketDTO.train_date=%s&' \
              'leftTicketDTO.from_station=%s&' \
              'leftTicketDTO.to_station=%s&' \
              'purpose_codes=ADULT' \
              % (date, from_station, to_station)
        warnings.filterwarnings('ignore')
        response = requests.get(url)
        # 获取到记录列车信息的列表
        raw_trains = response.json()['data']['result']
        for raw_train in raw_trains:
            raw_train_list = raw_train.split('|')
            # 获取车次编号的首字母小写
            self.train_number = raw_train_list[3]
            initial = self.train_number[0].lower()

            # 检查是否为用户输入的车次型号
            if not options or initial in options:
                self.from_station_code = raw_train_list[6]
                self.to_station_code = raw_train_list[7]
                self.start_time = raw_train_list[8]
                self.arrive_time = raw_train_list[9]
                self.time_duration = raw_train_list[10]
                self.first_class_seat = raw_train_list[31] or "--"
                self.second_class_seat = raw_train_list[30] or "--"
                self.soft_sleep = raw_train_list[23] or "--"
                self.hard_sleep = raw_train_list[28] or "--"
                self.hard_seat = raw_train_list[29] or "--"
                self.no_seat = raw_train_list[33] or "--"
            self.table._set_field_names('车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座'.split())
            self.table.add_row([
                # 输入到表格中
                self.train_number,
                '\n'.join([self.station.get_key(self.from_station_code), self.station.get_key(self.to_station_code)]),
                '\n'.join([self.start_time, self.arrive_time]),
                self.time_duration,
                self.first_class_seat,
                self.second_class_seat,
                self.soft_sleep,
                self.hard_sleep,
                self.hard_seat,
                self.no_seat
            ])
            print(self.table)
