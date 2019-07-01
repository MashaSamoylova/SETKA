from pyb import Pin, Timer, UART

from mainconfig import extruder_pulse_pin, first_head_pulse_pin,\
                       second_head_pulse_pin, reciever_pulse_pin,\
                       motors_enable_pin, reciever_enable_pin,\
                       owen_inputs, owen_addres
from makhina.motor import Motor
import random

import uasyncio as asyncio

class Makhina:

    # Work in progress
    wip = False

    def __init__(self):
        self.extrudo_engine = Motor(Timer(10), Pin(extruder_pulse_pin, Pin.OUT), 5000, 1)
        self.first_head_engine = Motor(Timer(8), Pin(first_head_pulse_pin, Pin.OUT), 18000, 3)
        self.second_head_engine = Motor(Timer(1), Pin(second_head_pulse_pin, Pin.OUT), 18000, 1)
        self.reciever_engine = Motor(Timer(4), Pin(reciever_pulse_pin, Pin.OUT), 3200, 1)

        self.engines = [self.extrudo_engine, self.first_head_engine,
                        self.second_head_engine, self.reciever_engine]

        # Подаем питание на шаговики
        self.enablePulse = Pin(motors_enable_pin, Pin.OUT)
        self.enablePulseReceiver = Pin(reciever_enable_pin, Pin.OUT)
        self.enablePulse.value(1)
        self.enablePulseReceiver.value(1)

    def start(self):
        self.wip = True
        self.enablePulse.value(0)
        self.enablePulseReceiver.value(0)
        for engine in self.engines:
            engine.accel_status = True

    def stop(self):
        self.wip = False
        self.enablePulse.value(1)
        self.enablePulseReceiver.value(1)
        for engine in self.engines:
            engine.stop()

class Owen:
    def __init__(self, server, control):
        self.server = server
        self.control = control

    async def read_owen_data(self):
        print("read from owen")
        '''new_nums = [random.randint(0, 1000) for _ in range(4)]
        self.control.log_new_data(new_nums)
        await asyncio.sleep_ms(60 * 1000)'''
        new_nums = []
        print(owen_inputs)
        for inpt in owen_inputs:
                try:
                    new_data = await self.server.connection.read_holding_registers(owen_addres, (inpt-1)*6, 2)
                    print("read from register:", new_data)
                    pointer_index, data = new_data
                    print("data", data)
                    new_num = float(str(data)[:-pointer_index] + "." + str(data)[:pointer_index])
                    self.control.owen_is_broken = False
                except Exception as e:
                    print(e, 'OWEN is broken')
                    self.control.owen_is_broken = True
                else:
                    new_nums.append(new_num)

        if len(new_nums) == 4:
            if not self.control.makhina.wip:
                print(new_nums)
                self.control.update_data_withput_logging(new_nums)
            else:
                self.control.log_new_data(new_nums)
