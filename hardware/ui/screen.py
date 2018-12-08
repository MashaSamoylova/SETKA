from ui.views import Button
from ui.tab1 import Tab1
from ui.tab2 import Tab2
from ui.tab3 import Tab3
from ui.utils import colors

import uasyncio as asyncio

import gc

class Screen:
    """Main screen"""

    current_tab_number = 0
    status_error = False
    error_msg = ""
    current_error = -1

    def __init__(self, lcd, makhina_control):
        self.lcd = lcd
        self.tab_buttons = [Button(lcd, 42 * i, 0, 42, 20, str(i + 1)) for i in range(3)]
        self.tab_buttons[0].handler = lambda: 1
        self.tab_buttons[1].handler = lambda: 2
        self.tab_buttons[2].handler = lambda: 3
        print(gc.mem_free())
        self.makhina_control = makhina_control
        self.tabs = [Tab1(lcd, makhina_control), Tab2(lcd), Tab3(lcd, makhina_control)]

        self.error_button = Button(lcd, 0, 125, 128, 30, "")
        self.error_button.handler = self.notify_error

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

        self.errors = [
                self.hot_melt_error, 
                self.high_pressure_error, 
                self.low_raw_material_error, 
                self.break_arm_error, 
                self.mesh_thickness_error
                ]

        loop = asyncio.get_event_loop()
        loop.create_task(self.handle_lcd_touch())
        loop.create_task(self.check_errors())
        loop.create_task(self.skip_errors())
        loop.create_task(self.unset_notify_client())


    def draw(self):
        """Draw tab buttons, errors and current tab"""

        for i, tab_button in enumerate(self.tab_buttons):
            if i == self.current_tab_number:
                tab_button.draw_touched()
            else:
                tab_button.draw_normal()
        self.tabs[self.current_tab_number].draw()
        if self.status_error:
            self.draw_error()        

    async def handle_lcd_touch(self):
        while True:
            touch, x, y = self.lcd.get_touch()
            if touch: 
                result = self.handle_touch(x, y)
                if result:
                    self.draw()
                    await asyncio.sleep_ms(200)
            await asyncio.sleep_ms(50)

    def handle_touch(self, x, y):
        """Delegates touch handling to error_button,
           then to buttons and then to current tab"""

        if self.status_error and self.error_button.handle_touch(x,y): return 1
        for button in self.tab_buttons:
            result = button.handle_touch(x, y)
            if result: break
        if result and self.current_tab_number != result - 1:
                self.tabs[self.current_tab_number].clear()
                self.current_tab_number = result - 1
                return result
        else:
            return self.tabs[self.current_tab_number].handle_touch(x, y)

    def draw_error(self):
        self.error_button.draw(colors["black"], colors["red"])

    def notify_error(self):
        self.error_button.draw(colors["red"], colors["white"])
        print("current_error", self.current_error)
        self.errors[self.current_error].notify_client = True
        return 1

    async def check_errors(self):
        while True:
            for i in range(len(self.errors)):
                if not self.errors[i].active and self.errors[i].check():
                    self.errors[i].primary_handler()
                    self.errors[i].active = True
                    self.current_error = i
            await asyncio.sleep_ms(1000)

    async def skip_errors(self):
        while True:
            for i in range(len(self.errors)):
                if self.errors[i].skip() and self.errors[i].active:
                    self.errors[i].active = False
                    self.current_error = self.get_next_error()
                    if self.current_error == -1:
                        self.error_button.clear()
                        self.status_error = False
                        self.draw()
                    else:
                        self.set_status_error(self.errors[self.current_error].code)
            await asyncio.sleep_ms(1000) 

    async def unset_notify_client(self):
        while True:
            for e in self.errors:
                e.notify_client = False
            await asyncio.sleep_ms(10 * 60 * 1000)

    def get_next_error(self):
        for i in range(len(self.errors)):
            if self.errors[i].active:
                return i
        return -1

    def set_status_error(self, code):
        self.status_error = True
        self.error_button.text = str(code)


###########################################
# HOT MELT
###########################################
    def hot_melt_check(self):
        temperature1 = float(self.tabs[1].temperature1.text)
        temperature2 = float(self.tabs[1].temperature2.text)
        if temperature1  > 100 or temperature2 > 100:
            #self.tabs[1].temperature1.text = "000.0"
            return True
        return False

    def hot_melt_primary_handler(self):
        self.set_status_error("1")
        self.makhina_control.stop()
        self.draw()

    def skip_hot_melt(self):
        temperature1 = float(self.tabs[1].temperature1.text)
        temperature2 = float(self.tabs[1].temperature2.text)
        print("notify client", self.hot_melt_error.notify_client)
        if temperature1  <=  100 and temperature2  <= 100 and self.hot_melt_error.notify_client:
            self.hot_melt_error.notify_client = False
            return True
        return False

###########################################
# HIGH PRESSURE 
###########################################
    def high_pressure_check(self):
        pressure1 = float(self.tabs[1].pressure1.text)
        pressure2 = float(self.tabs[1].pressure2.text)
        if pressure1 > 100 or pressure2 > 100:
            return True
        return False

    def high_pressure_primary_handler(self):
        self.set_status_error("1")
        self.makhina_control.stop()
        self.draw()

    def skip_high_pressure(self):
        pressure1 = float(self.tabs[1].pressure1.text)
        pressure2 = float(self.tabs[1].pressure2.text)
        if pressure1 <= 100 or pressure2 <= 100 and self.high_pressure_error.notify_client:
            self.high_pressure_error.notify_client = False
            return True
        return False

############################################
# LOW RAW MATERIAL
############################################
    def low_raw_material_check(self):
        if not machine.Pin("X8", machine.Pin.IN, machine.Pin.PULL_UP).value() and not self.low_raw_material_error.notify_client:
            return True
        return False

    def low_raw_primary_handler(self):
        pass

    def skip_low_raw_material(self):
        if machine.Pin("X7", machine.Pin.In, machine.Pin.PULL_UP).value() or self.low_raw_material_error.notify_client:
            return True
        return False

############################################
# BREAK ARM
############################################
    def break_arm_check(self):
        if not machine.Pin("X8", machine.Pin.In, machine.Pin.PULL_UP).value() and not self.break_arm_error.notify_client:
            return True
        return False

    def break_arm_primary_nandler(self):
        pass

    def skip_break_arm(self):
        if machine.Pin("X8", machine.Pin.In, machine.Pin.PULL_UP).value() or self.break_arm_error.notify_client:
            return True
        return False


#############################################
# MESH THICKNESS
#############################################
    def mesh_thickness_check(self):
        mt = float(self.tabs[2].mesh_thickness.text)
        if mt > 100:
            return True
        return False

    def mesh_thickness_primary_handler(self):
        pass

    def skip_mesh_thickness(self):
        mt = float(self.tabs[2].mesh_thickness.text)
        if mt <= 100 and self.mesh_thickness_error.notify_client:
            self.mesh_thickness_error.notify_client = False
            return True
        return False 

class Error():
    primary_handler = lambda: 1
    skip = lambda: 1
    check = lambda: 1
    active = False
    notify_client = False

    def __init__(self, code):
        self.code = code

