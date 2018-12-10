from pyb import Pin, Timer, UART

from mainconfig import extruder_pulse_pin, first_head_pulse_pin,\
                       second_head_pulse_pin, reciever_pulse_pin,\
                       motors_enable_pin, reciever_enable_pin, mesh_uart_number
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

        self.mesh_thikness_uart = UART(mesh_uart_number, 9600, timeout=200)
        self.mesh_thikness = 0

        loop = asyncio.get_event_loop()
        loop.create_task(self.update_mesh())
    
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

    async def update_mesh(self):
        while True:
            if self.wip and self.mesh_thikness_uart.any():
                self.mesh_thikness = self.mesh_thikness_uart.read()

            await asyncio.sleep_ms(2000)


owen_pins = [1, 2, 3, 4]
owen_addres = 16

class Owen:
    def __init__(self, server, control):
        self.server = server
        self.control = control

    async def read_owen_data(self):
        if not self.control.makhina.wip:
            return
        """try:
            new_data = await self.server.connection.read_holding_registers(owen_addres, 0, 48)
        except Exception as e:
            print(e, 'OWEN is broken')
        else:
            print(new_data)
            new_data = [new_data[pin * 6 + 1] for pin in owen_pins]
            print(new_data)
        """
        new_data = [random.randint(0, 1000) for _ in range(4)]
        self.control.log_new_data(new_data)
        await asyncio.sleep_ms(60 * 1000)
