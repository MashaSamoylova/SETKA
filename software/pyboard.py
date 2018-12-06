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
    cmd = None
    extruder_speed = ['' for i in range(5)]
    first_head_speed = ['' for i in range(5)]
    second_head_speed = ['' for i in range(5)]
    reciever_speed = ['' for i in range(5)]
    config = ['' for i in range(5)]

    def __init__(self):
        pass

    def on_connected(self, slave_id, function_code, address, value):
        if value == 1:
            print('PYBOARD CONNECTED')
            self.connected = True
            self.build_server()

    def build_server(self):
        self.server.route_map.add_rule(self.on_read_reg, [5], [3], [2])
        self.server.route_map.add_rule(self.on_write_reg, [5], [16], list(range(256)))
        self.cmd = 0x2

    def on_read_reg(self, slave_id, function_code, address):
        print('address', address)
        if address == 2:
            return self.cmd

    def on_write_reg(self, slave_id, function_code, address, value):
        print(address, chr(value))
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

    def connect(self, port, callback):
        self.server = get_server(RTUServer, serial.Serial(port))
        self.server.route_map.add_rule(self.on_connected, [5], [5], [1])
        while not self.connected:
            print('Trying to connect')
            try:
                self.server.serve_once()
            except:
                print('No response')
            time.sleep(1)
        callback(1)

    def run(self):
        while True:
            if self.connected:
                try:
                    self.server.serve_once()
                except Exception as e:
                    print(e)
            time.sleep(0.1)

