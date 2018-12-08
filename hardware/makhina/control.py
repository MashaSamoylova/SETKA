import machine
from pyb import RTC

import uasyncio as asyncio

from mainconfig import up_button_pin, down_button_pin,\
                       right_button_pin, start_button_pin, stop_button_pin
from makhina.makhina import Makhina
from ui.utils import count_time_diff, zfill, chunkstring, to_float

class MakhinaControl:

    log = None
    log_name = ''
    log_time = None
    t1 = '000.0'
    t2 = '000.0'
    p1 = '000.0'
    p2 = '000.0'
    config = '000'
    extrudo_speed = ""
    first_head_speed = ""
    second_head_speed = ""
    reciever_speed = ""

    def __init__(self):
        self.makhina = Makhina()
        
        self.plus_button = AnalogButton(up_button_pin)
        self.minus_button = AnalogButton(down_button_pin)
        self.right_button = AnalogButton(right_button_pin)
        self.start_button = AnalogButton(start_button_pin)
        self.stop_button = AnalogButton(stop_button_pin)

        self.start_button.handler = self.start
        self.stop_button.handler = self.stop

        # скорости в форме строки, чтобы не переводить из частоты обратно

        self.change_current_config('000')
        self.rtc = RTC()
        print("INIT SPEEDS")

    def start_new_log(self):
        if self.log: self.log.close()
        *_, month, day, _, hours, minutes, seconds, _ = self.rtc.datetime()
        self.log_time = (month, day, hours, minutes, seconds)
        self.log_name = '.'.join(zfill(str(x), 2) for x in self.log_time)
        self.log = open('/sd/logs/' + self.log_name, 'w')

    def log_new_data(self, new_data):
        self.t1, self.t2, self.p1, self.p2 = new_data
        *_, month, day, _, hours, minutes, seconds, _ = self.rtc.datetime()
        new_time = (month, day, hours, minutes, seconds)
        if count_time_diff(self.log_time, new_time) // 60 >= 1:
            self.start_new_log()
        self.log.write(''.join([to_float(x) for x in new_data]) + '\n')

    def start(self):
        self.makhina.start()
        self.start_new_log()

    def stop(self):
        self.makhina.stop()

    def set_speeds(self, speeds):
        self.extrudo_speed, self.first_head_speed, self.second_head_speed, self.reciever_speed = speeds
        print('Speeds in set speeds', speeds)

        self.makhina.extrudo_engine.set_round_per_min(float(self.extrudo_speed))
        self.makhina.first_head_engine.set_round_per_min(float(self.first_head_speed))
        self.makhina.second_head_engine.set_round_per_min(float(self.second_head_speed))
        self.makhina.reciever_engine.set_round_per_min(float(self.reciever_speed))

        with open("/sd/recipes/" + self.config, "w") as f:
            f.write("".join(list(map(to_float, [self.extrudo_speed, self.first_head_speed,
                             self.second_head_speed, self.reciever_speed]))))
            print("writing at /sd/recipes/" + self.config)

    def change_current_config(self, config):
        self.config = zfill(str(config), 3)
        print("current_config", self.config)
        try:
            with open("/sd/recipes/" + self.config) as f:
                speeds = f.read()
        except:
            with open("/sd/recipes/" + self.config, "w") as f:
                speeds = "000.0" * 4
                f.write(speeds)

        self.extrudo_speed, self.first_head_speed, self.second_head_speed, self.reciever_speed = chunkstring(speeds, 5)
        self.set_speeds((self.extrudo_speed, self.first_head_speed, self.second_head_speed, self.reciever_speed))

class AnalogButton:

    handler = lambda : 1
    enabled = True

    def __init__(self, pin):
        self.button = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        loop = asyncio.get_event_loop()
        loop.create_task(self.handle_touch())

    async def handle_touch(self):
        while True:
            await asyncio.sleep_ms(50)
            if self.enabled and not self.button.value():
                self.handler()
                await asyncio.sleep_ms(200)
