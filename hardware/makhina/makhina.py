from pyb import Pin, Timer

from mainconfig import extruder_pulse_pin, first_head_pulse_pin,\
                       second_head_pulse_pin, reciever_pulse_pin,\
                       motors_enable_pin, reciever_enable_pin
from makhina.motor import Motor

class Makhina:

    # Work in progress
    wip = True

    def __init__(self):
        self.extrudo_engine = Motor(Timer(2), Pin(extruder_pulse_pin, Pin.OUT), 5000, 3)
        self.first_head_engine = Motor(Timer(3), Pin(first_head_pulse_pin, Pin.OUT), 18000, 4)
        self.second_head_engine = Motor(Timer(1), Pin(second_head_pulse_pin, Pin.OUT), 18000, 1)
        self.reciever_engine = Motor(Timer(4), Pin(reciever_pulse_pin, Pin.OUT), 3200, 1)

        self.engines = [self.extrudo_engine, self.first_head_engine,
                        self.second_head_engine, self.reciever_engine]

        # Подаем питание на шаговики
        self.enablePulse = Pin(motors_enable_pin, Pin.OUT)
        self.enablePulseReceiver = Pin(reciever_enable_pin, Pin.OUT)
        self.enablePulse.low()
        self.enablePulseReceiver.low()
    
    def start(self):
        self.wip = True
        for engine in self.engines:
            engine.accel_status = True
            engine.accel()

    def stop(self):
        self.wip = False
        for engine in self.engines:
            engine.stop()

owen_pins = [1, 2, 3, 4]
owen_addres = 16

class Owen:
    def __init__(self, server, control):
        self.server = server
        self.control = control

    async def read_owen_data(self):
        if not self.control.makhina.wip:
            return
        try:
            new_data = await self.server.connection.read_holding_registers(owen_addres, 0, 48)
        except Exception as e:
            print(e, 'OWEN is broken')
        else:
            print(new_data)
            new_data = [new_data[pin * 6 + 1] for pin in owen_pins]
            print(new_data)
            t1, t2, p1, p2, *_ = new_data
            self.control.log_new_data(new_data)
