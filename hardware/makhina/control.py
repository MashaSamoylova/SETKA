import machine
from pyb import RTC

import uasyncio as asyncio

from mainconfig import up_button_pin, down_button_pin,\
                       right_button_pin, start_button_pin, stop_button_pin,\
                       max_pressure, level_material_pin, break_arm_pin, assertion_pin,\
                       emergency_stop_pin, high_temperature_pin, log_length,\
                       max_extruder_round, max_first_head_round,\
                       max_second_head_round, max_reciver_round 


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
    extrudo_speed = "000.0"
    first_head_speed = "00.0"
    second_head_speed = "00.0"
    reciever_speed = "00.0"
    current_error = -1

    def __init__(self):
        self.makhina = Makhina()
        
        self.plus_button = AnalogButton(up_button_pin)
        self.minus_button = AnalogButton(down_button_pin)
        self.right_button = AnalogButton(right_button_pin)
        self.start_button = AnalogButton(start_button_pin)
        self.stop_button = AnalogButton(stop_button_pin)
        self.level_material = machine.Pin(level_material_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.break_arm = machine.Pin(break_arm_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.emergency_stop = machine.Pin(emergency_stop_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.high_temperature = machine.Pin(high_temperature_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.assertion = machine.Pin(assertion_pin, machine.Pin.OUT)
        self.assertion.value(0)

        self.start_button.handler = self.start
        self.stop_button.handler = self.stop

        self.change_current_config('000')
        self.rtc = RTC()
        print("INIT SPEEDS")

        self.high_pressure_error = Error(2)
        self.high_pressure_error.check = self.high_pressure_check
        self.high_pressure_error.primary_handler = self.high_pressure_primary_handler
        self.high_pressure_error.skip = self.skip_high_pressure

        self.low_raw_material_error = Error(3)
        self.low_raw_material_error.check = self.low_raw_material_check
        self.low_raw_material_error.primary_handler = self.low_raw_primary_handler
        self.low_raw_material_error.skip = self.skip_low_raw_material

        self.break_arm_error = Error(4)
        self.break_arm_error.check = self.break_arm_check
        self.break_arm_error.primary_handler = self.break_arm_primary_nandler
        self.break_arm_error.skip = self.skip_break_arm

        self.emergency_stop_error = Error(5)
        self.emergency_stop_error.check = self.emergency_stop_check
        self.emergency_stop_error.primary_handler = self.emergency_stop_primary_handler
        self.emergency_stop_error.skip = self.skip_emergency_stop

        self.errors = [
                self.high_pressure_error,
                self.low_raw_material_error,
                self.break_arm_error,
                self.emergency_stop_error,
                ]

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
        if count_time_diff(self.log_time, new_time) // 60 >= log_length:
            self.start_new_log()
        print("writing in log")
        self.log.write(zfill(str(hours), 2) + zfill(str(minutes), 2)\
                       + ''.join([to_float(x) for x in new_data]) + '\n')
        self.log.flush()

    def start(self):
        self.makhina.start()
        self.start_new_log()

    def stop(self):
        self.makhina.stop()

    def assertion_client(self):
        print("ASERTION")
        self.assertion.value(1)

    def stop_assertion(self):
        print("STOP ASERTION")
        self.assertion.value(0)

    def check_max(self):
        print("check max")
        if float(self.extrudo_speed) > max_extruder_round:
            self.extrudo_speed = str(max_extruder_round)
        if float(self.first_head_speed) > max_first_head_round:
            self.first_head_speed = str(max_first_head_round)
        if float(self.second_head_speed) > max_second_head_round:
            self.second_head_speed = str(max_second_head_round)
        if float(self.reciever_speed) > max_reciver_round:
            self.reciever_speed = str(max_reciver_round)

    def set_speeds(self, speeds):
        self.extrudo_speed, self.first_head_speed, self.second_head_speed, self.reciever_speed = speeds
        self.check_max()

        print('Speeds in set speeds', self.extrudo_speed)

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
        self.first_head_speed = self.first_head_speed[1:]
        self.second_head_speed = self.second_head_speed[1:]
        self.reciever_speed = self.reciever_speed[1:]
        self.set_speeds((self.extrudo_speed, self.first_head_speed, self.second_head_speed, self.reciever_speed))

###########################################
# HIGH PRESSURE
###########################################
    def high_pressure_check(self):
        if float(self.p1) > max_pressure or float(self.p2) > max_pressure:
            return True
        return False

    def high_pressure_primary_handler(self):
        self.stop()

    def skip_high_pressure(self):
        if (float(self.p1) <= max_pressure or float(self.p2) <= max_pressure) and self.high_pressure_error.notify_client:
            self.high_pressure_error.notify_client = False
            return True
        return False

############################################
# LOW RAW MATERIAL
############################################
    def low_raw_material_check(self):
        if not self.level_material.value() and not self.low_raw_material_error.notify_client:
            return True
        return False

    def low_raw_primary_handler(self):
        pass

    def skip_low_raw_material(self):
        if self.level_material.value() or self.low_raw_material_error.notify_client:
            return True
        return False

############################################
# BREAK ARM
############################################
    def break_arm_check(self):
        if not self.break_arm.value() and not self.break_arm_error.notify_client:
            return True
        return False

    def break_arm_primary_nandler(self):
        pass

    def skip_break_arm(self):
        if self.break_arm.value() or self.break_arm_error.notify_client:
            return True
        return False

#############################################
# EMERGENCY STOP
#############################################
    def emergency_stop_check(self):
        if not self.emergency_stop.value():
            return True
        return False

    def emergency_stop_primary_handler(self):
        pass

    def skip_emergency_stop(self):
        if self.emergency_stop.value() and self.emergency_stop_error.notify_client:
            return True
        return False


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


class Error():
    primary_handler = lambda: 1
    skip = lambda: 1
    check = lambda: 1
    active = False
    notify_client = False

    def __init__(self, code):
        self.code = code
