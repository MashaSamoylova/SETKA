import logging
from collections import defaultdict
import time

import serial
from umodbus import conf
from umodbus.server.serial import get_server
from umodbus.server.serial.rtu import RTUServer
from umodbus.utils import log_to_stream
import os

class PyBoard():

    server = None
    connected = None
    cmd = 0
    arg = 0
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

    def __init__(self):
        pass

    def on_connected(self, slave_id, function_code, address, value):
        if value == 1:
            print('PYBOARD CONNECTED')
            self.connected = True
            self.build_server()

    def build_server(self):
        self.server.route_map.add_rule(self.on_read_reg, [5], [3], list(range(256)))
        self.server.route_map.add_rule(self.on_write_reg, [5], [16], list(range(256)))
        self.server.route_map.add_rule(self.on_write_single_reg, [5], [6], list(range(256)))

    def on_read_reg(self, slave_id, function_code, address):
        if address == 2:
            return self.cmd
        if address == 3:
            return self.arg
        if address in list(range(50, 70)):
            return ord(self.config_value[address - 50])

    def on_write_single_reg(self, slave_id, function_code, address, value):
        if address == 2:
            self.cmd = value
        if address == 3:
            self.arg = value

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
                except Exception as e:
                    print(e)
            time.sleep(0.05)
