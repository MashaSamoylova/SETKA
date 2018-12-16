import logging
from collections import defaultdict
import time
from datetime import datetime

import serial
from umodbus import conf
from umodbus.server.serial import get_server
from umodbus.server.serial.rtu import RTUServer
from umodbus.utils import log_to_stream
import os

error_map = ["Перегрев расплава/Аварийная остановка",
             "Превышено давление",
             "Низкий уровень сырья",
             "Обрыв рукава",
             "Аварийная остановкаa"]

class PyBoard():

    server = None
    connected = None
    cmd = 0
    arg = 0
    master_arg = 0
    recieve_flag = 0
    extruder_speed = ['' for i in range(5)]
    first_head_speed = ['' for i in range(5)]
    second_head_speed = ['' for i in range(5)]
    reciever_speed = ['' for i in range(5)]
    config = ['' for i in range(5)]
    config_value = list('000.0' * 4)
    t1 = list("000.0")
    t2 = list("000.0")
    p1 = list("000.0")
    p2 = list("000.0")
    buff_len = 80
    recieved_file = None
    current_download = 0
    chosen_log_name = list('0'*10)
    error_status = 0
    last_operation = 0
    params = [-1 for i in range(5)]
    errors_in_a_row = 0

    def __init__(self):
        self.buffer_string = [-1 for x in range(self.buff_len)]

    def on_connected(self, slave_id, function_code, address, value):
        if value == 1:
            print('PYBOARD CONNECTED')
            self.connected = True
            self.build_server()

    def build_server(self):
        self.server.route_map.add_rule(self.on_read_reg, [5], [3], list(range(256)))
        self.server.route_map.add_rule(self.on_write_reg, [5], [16], list(range(100 + self.buff_len + 1)))
        self.server.route_map.add_rule(self.on_write_single_reg, [5], [6], list(range(256)))

    def on_read_reg(self, slave_id, function_code, address):
        if address == 2:
            return self.cmd
        if address == 3:
            return self.arg
        if address == 4:
            return self.master_arg
        if address == 99:
            return self.recieve_flag
        if address in list(range(50, 70)):
            return ord(self.config_value[address - 50])
        if address in list(range(70, 80)):
            return ord(self.chosen_log_name[address - 70])

    def on_write_single_reg(self, slave_id, function_code, address, value):
        if address == 2:
            self.cmd = value
        if address == 3:
            self.arg = value
        if address == 4:
            self.master_arg = value
        if address >= 90 and address < 96:
            self.params[address - 90] = value
        if address == 98:
            if self.error_status != value:
                if self.error_status:
                    with open('log.txt', 'a') as f:
                        f.write('{} Вход в состояние ошибки {}: {}'.format(datetime.today().strftime("%Y-%m-%d %H:%M:%S"), value,
                                                                    error_map[value - 2]) + '\n')
                else:
                    with open('log.txt', 'a') as f:
                        f.write('{} Все ошибки квитированы'.format(datetime.today().strftime("%Y-%m-%d %H:%M:%S")) + '\n')
            self.error_status = value
        if address == 99:
            self.recieve_flag = value

    def on_write_reg(self, slave_id, function_code, address, value):
        if address in list(range(5, 10)):
            self.extruder_speed[address % 5] = chr(value)
        if address in list(range(10, 15)):
            self.first_head_speed[address % 5] = chr(value)
        if address in list(range(15, 20)):
            self.second_head_speed[address % 5] = chr(value)
        if address in list(range(20, 25)):
            self.reciever_speed[address % 5] = chr(value)
        if address in list(range(25, 30)):
            self.config[address % 5] = chr(value)
        if address in list(range(30, 35)):
            self.t1[address % 5] = chr(value)
        if address in list(range(35, 40)):
            self.t2[address % 5] = chr(value)
        if address in list(range(40, 45)):
            self.p1[address % 5] = chr(value)
        if address in list(range(45, 50)):
            self.p2[address % 5] = chr(value)
        if address in list(range(50, 70)):
            self.config_value[address - 50] = chr(value)
        if address >= 100 and address < 100 + self.buff_len:
            self.buffer_string[address - 100] = value

    def flush_buffer(self):
        local_buffer = [x for x in self.buffer_string if x != -1]
        self.buffer_string = [-1 for x in range(self.buff_len)]
        return local_buffer

    def recieve_logs_list(self):
        params = [-1 for i in range(5)]
        self.recieve_flag = 0
        self.recieved_file = list()
        self.current_download = 0
        self.cmd = 5

    def download_existing(self):
        params = [-1 for i in range(5)]
        self.recieve_flag = 0
        self.recieved_file = list()
        self.current_download = 0
        self.cmd = 7

    def download_log(self, log_name):
        params = [-1 for i in range(5)]
        print("log name", log_name)
        self.chosen_log_name = list(log_name.replace('.', ''))
        self.recieved_flag = 0
        self.recieved_file = list()
        self.current_download = 0
        self.cmd = 6

    def connect(self, port, callback):
        try:
            self.server = get_server(RTUServer, serial.Serial(port, baudrate=115200))
        except:
            callback(0)
            return 0
        self.server.route_map.add_rule(self.on_connected, [5], [5], [1])
        while not self.connected:
            print('Trying to connect')
            try:
                self.server.serve_once()
            except:
                print('No response')
            time.sleep(0.1)
        callback(1)

    def run(self):
        while True:
            if self.connected:
                try:
                    self.server.serve_once()
                except ValueError:
                    pass
                except Exception as e:
                    print(e)
                    self.errors_in_a_row += 1
                    if self.errors_in_a_row > 10:
                        self.connected = False
                else:
                    self.errors_in_a_row = 0
                print('recieve', self.recieve_flag)
                if self.recieve_flag > 0:
                    self.recieved_file += self.flush_buffer()
                    print("FILE", self.recieved_file)
                if self.recieve_flag == 2:
                    self.cmd = 0
                    self.recieve_flag = -1
                    self.last_operation = 1
                elif self.recieve_flag == 3:
                    self.cmd = 0
                    self.recieve_flag = -1
                    self.last_operation = 0
                elif self.recieve_flag == 5:
                    self.cmd = 0
                    self.recieve_flag = -1
                    self.last_operation = 0
                else:
                    self.recieve_flag = 0
                    self.current_download += 1
                time.sleep(0.05)
