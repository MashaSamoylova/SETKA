import pyb
import math


class Motor:
    
    impulse_width = 9000
    __gz_current = 0
    __gz_new = 0

    def __init__(self, timer, pin, const, channel):
        self.timer = timer
        self.pin = pin
        self.pin.low()
        #константа количество импульсов для одного оборота
        self.const = const
        self.channel = channel

    def set_round_per_min(self, rpm):
        print(rpm)
        self.__gz_new = int(rpm * (self.const / 60))

        while rpm > (self.__gz_new / (self.const / 60)):
            self.__gz_new = self.__gz_new + 1
 
    def accel(self):
        print("accel")
        print("new:", self.__gz_new)
        print("current: ", self.__gz_current)
        if not self.__gz_current and self.__gz_new > self.__gz_current:
            print("ускорение")
            self.timer.init(freq=1)
            ch = self.timer.channel(self.channel, pyb.Timer.PWM, pin=self.pin, pulse_width=self.impulse_width)
        
        if self.__gz_new > self.__gz_current:
            diff = int(math.sqrt(self.__gz_new - self.__gz_current))
            self.__gz_current = self.__gz_current + int(diff)
            self.timer.freq(self.__gz_current)
        else:
            self.__gz_current = self.__gz_new

        if not self.__gz_current:
            self.timer.deinit()
        else:
            self.timer.freq(self.__gz_current)
    
    def stop(self):
        print("stop")
        self.__gz_current = 0
        print("stop:", self.__gz_new)
        print("stop:", self.__gz_current)
        self.timer.deinit()
