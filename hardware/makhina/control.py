import machine
from pyb import RTC

import uasyncio as asyncio

from mainconfig import up_button_pin, down_button_pin,\
                       right_button_pin, start_button_pin, stop_button_pin,\
                       max_pressure, level_material_pin, break_arm_pin,\
                       emergency_stop_pin, high_temperature_pin
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
        self.level_material = machine.Pin(level_material_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.break_arm = machine.Pin(break_arm_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.emergency_stop = machine.Pin(emergency_stop_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.high_temperature = machine.Pin(high_temperature_pin, machine.Pin.IN, machine.Pin.PULL_UP)

        self.start_button.handler = self.start
        self.stop_button.handler = self.stop

        # скорости в форме строки, чтобы не переводить из частоты обратно

        self.change_current_config('000')
        self.rtc = RTC()
        print("INIT SPEEDS")

        self.hot_melt_error = Error(1)
        self.hot_melt_error.check = self.hot_melt_check
        self.hot_melt_error.primary_handler = self.hot_melt_primary_handler
        self.hot_melt_error.skip = self.skip_hot_melt

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

        self.mesh_thickness_error = Error(5)
        self.mesh_thickness_error.check = self.mesh_thickness_check
        self.mesh_thickness_error.primary_handler = self.mesh_thickness_primary_handler
        self.mesh_thickness_error.skip = self.skip_mesh_thickness

        self.emergency_stop_error = Error(6)
        self.emergency_stop_error.check = self.emergency_stop_check
        self.emergency_stop_error.primary_handler = self.emergency_stop_primary_handler
        self.emergency_stop_error.skip = self.skip_emergency_stop

        self.errors = [
                self.hot_melt_error,
                self.high_pressure_error,
                self.low_raw_material_error,
                self.break_arm_error,
                self.mesh_thickness_error,
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
        if count_time_diff(self.log_time, new_time) // 60 >= 1:
            self.start_new_log()
        print("writing in log")
        self.log.write(zfill(str(hours), 2) + zfill(str(minutes), 2)\
                       + ''.join([to_float(x) for x in new_data]) + '\n')

    def start(self):
        self.makhina.start()
        self.start_new_log()
        print("MAKHINA STAAAAAAAAAAAAART")

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

###########################################
# HOT MELT
###########################################
    def hot_melt_check(self):
        if not self.high_temperature.value():
            return True
        return False

    def hot_melt_primary_handler(self):
        self.stop()

    def skip_hot_melt(self):
        print("SKIP", self.hot_melt_error.notify_client)
        if self.high_temperature.value() and self.hot_melt_error.notify_client:
            self.hot_melt_error.notify_client = False
            return True
        return False

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
        if float(self.p1) <= max_pressure or float(self.p2) <= max_pressure and self.high_pressure_error.notify_client:
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
# MESH THICKNESS
#############################################
    def mesh_thickness_check(self):
        return False
        pass
      #  mt = float(self.makhina.mesh_thikness)
       # if mt > max_mesh_thickness:
       #     return True
       # return False

    def mesh_thickness_primary_handler(self):
        pass

    def skip_mesh_thickness(self):
        return False
        pass
       # mt = float(self.makhina.mesh_thikness)
        #if mt <= max_mesh_thickness and self.mesh_thickness_error.notify_client:
         #   self.mesh_thickness_error.notify_client = False
         #   return True
        #return False

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
