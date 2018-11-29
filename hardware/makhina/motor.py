import pyb
import math


class Motor:
    def __init__(self, timer, pin, const, channel):
        self.timer = timer
        self.pin = pin
        self.pin.low()
        #константа количество импульсов для одного оборота
        self.const = const
        self.channel = channel
        self.__gz_current = 0
        self.__gz_new = 0
        self.impulse_width = 9000

    def set_round_per_min(self, rpm):
        self.__gz_new = int(rpm * (self.const / 60))

        while rpm > (self.__gz_new / (self.const / 60)):
            self.__gz_new = self.__gz_new + 1
 
    def accel(self):
        if self.__gz_current == 0 and self.__gz_new > self.__gz_current:
            self.timer.init(freq=1)
            ch = self.timer.channel(self.channel, pyb.Timer.PWM, pin=self.pin, pulse_width=self.pulse_width)
        
        if self.__gz_new > self.__gz_current:
            diff = int(math.sqrt(self.__gz_new - self.__gz_current))
            self.__gz_current = self.__gz_current + int(diff)
            self.timer.freq(self.__gz_current)
        else:
            self.__gz_current = self.__gz_new

        if self.__gz_current == 0:
            self.timer.deinit()
        else:
            self.timer.freq(self.__gz_current)
    
    def stop(self):
        self.__gz_current == 0
        self.timer.deinit()
