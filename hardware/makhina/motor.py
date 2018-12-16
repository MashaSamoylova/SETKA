import pyb
import math

import uasyncio as asyncio
from mainconfig import acceleration_delay


class Motor:
    
    impulse_width = 9000
    __gz_current = 0
    __gz_new = 0
    accel_status = False

    def __init__(self, timer, pin, const, channel):
        self.timer = timer
        self.pin = pin
        self.pin.value(0)
        #константа количество импульсов для одного оборота
        self.const = const
        self.channel = channel
        loop = asyncio.get_event_loop()
        loop.create_task(self.run())

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
            pass
        else:
            self.timer.freq(self.__gz_current)
            pass

    async def run(self):
        while True:
            # accelfunction sets accel_status in False when __gz_current = __qz_new
            if self.accel_status:
                self.accel()
            await asyncio.sleep_ms(acceleration_delay)

    
    def stop(self):
        self.__gz_current = 0
        print("stop:", self.__gz_new)
        print("stop:", self.__gz_current)
        self.timer.deinit()
        self.accel_status = False

