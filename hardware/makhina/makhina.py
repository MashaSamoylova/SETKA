from pyb import Pin, Timer

from motor import Motor


class Makhina:
    def __init__(self):
        self.extrudo_engine = Motor(Timer(2), Pin('Y3', Pin.OUT), 5000, 3)
        self.first_head_engine = Motor(Timer(3), Pin('Y12', Pin.OUT), 18000, 4)
        self.second_head_engine = Motor(Timer(1), Pin('Y6', Pin.OUT), 18000, 1)
        self.reciever_engine = Motor(Timer(4), Pin('X9', Pin.OUT), 3200, 1))

        # Подаем питание на шаговики
        self.enablePulse = Pin('Y5', Pin.OUT)
        self.enablePulseReceiver = Pin('Y7', Pin.OUT)
        self.enablePulse.low()
        self.enablePulseReceiver.low()

