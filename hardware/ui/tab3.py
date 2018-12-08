from pyb import RTC

import uasyncio as asyncio

from ui.views import Button, EditableButton, Label
from ui.utils import colors, zfill


class Tab3:
    """Third tab, includes:
        white editable string - config name
        white editable string - time
        white editable string - date"""

    edit_mode = False
    is_draw = False
    cur_button = 0
    
    def __init__(self, lcd, makhina_control):
        self.mesh_thickness = Label(lcd, 45, 30, "56", fg=colors["blue"])
        self.config_string = EditableButton(lcd, 75, 50, 128, 17, makhina_control.config)
        self.time_string = EditableButton(lcd, 30, 80, 128, 17, "00:00:00")
        self.date_string = EditableButton(lcd, 5, 100, 128, 17, "00:00:00")

        self.settings_buttons = [self.config_string, self.time_string, self.date_string]
        self.analog_buttons = [makhina_control.plus_button,
                               makhina_control.minus_button,
                               makhina_control.right_button]
        for anal_butt in self.analog_buttons:
            anal_butt.enabled = False
        self.makhina_control = makhina_control
        self.time_string.font_size = 1
        self.date_string.font_size = 1

        self.change_button = Button(lcd, 0, 125, 128, 30, "Change")

        self.ok_button = Button(lcd, 0, 125, 64, 30, "Ok")
        self.cancel_button = Button(lcd, 64, 125, 64, 30, "Cnl")

        self.change_button.handler = self.change_handler
        self.ok_button.handler = self.ok_handler
        self.cancel_button.handler = self.cancel_handler

        self.rtc = RTC()
        loop = asyncio.get_event_loop()
        loop.create_task(self.timer())

    def draw(self):
        self.is_draw = True
        self.makhina_control.plus_button.handler = self.plus_handler
        self.makhina_control.minus_button.handler = self.minus_handler
        self.makhina_control.right_button.handler = self.right_handler
        self.config_string.draw_normal()
        self.time_string.draw_normal()
        self.date_string.draw_normal()
        if self.edit_mode:
            self.ok_button.draw_normal()
            self.cancel_button.draw_normal()
        else:
            self.change_button.draw_normal()
    
    def change_handler(self):
        self.edit_mode_on()
        return 1

    def toggle_button_highlight(self, n):
        if self.cur_button:
            self.settings_buttons[self.cur_button - 1].edit_mode = False
            self.settings_buttons[self.cur_button - 1].draw_normal()
        self.cur_button = 0 if n == self.cur_button else n

    def edit_mode_on(self):
        self.edit_mode = True
        self.toggle_button_highlight(1)
        self.settings_buttons[self.cur_button - 1].edit_mode = True
        for anal_butt in self.analog_buttons:
            anal_butt.enabled = True

    def edit_mode_off(self):
        self.edit_mode = False
        for anal_butt in self.analog_buttons:
            anal_butt.enabled = False
        if self.cur_button:
            self.settings_buttons[self.cur_button - 1].edit_mode = False
            self.settings_buttons[self.cur_button - 1].draw_normal()
        self.cur_button = 0

    def ok_handler(self):
        self.edit_mode_off()

        if self.makhina_control.config != self.config_string.text:
            print("CHANGED CONFIG", self.config_string.text)
            self.makhina_control.config = self.config_string.text
            self.makhina_control.change_current_config()
        
        hour, minute, second = self.time_string.text.split(":")
        year, month, day = self.date_string.text.split(":")

        self.rtc.datetime(list(map(int, [year, month, day, 0, 
                                    hour, minute, second, 0])))
        return 1

    def cancel_handler(self):
        self.edit_mode_off()
        return 1
    
    async def timer(self):
        while True:
            self.update_time()
            await asyncio.sleep_ms(1000)

    def update_time(self):
        if not self.edit_mode and self.is_draw:
            year, month, date, _, hour, minute, second, _ = self.rtc.datetime()
            self.time_string.text = ":".join([zfill(str(x), 2) for x in [hour, minute, second]])
            self.time_string.draw_normal()
            
            new_date = ":".join([zfill(str(x), 2) for x in [year, month, date]])
            if self.date_string.text != new_date:
                self.date_string.text = new_date
                self.date_string.draw_normal()

    def plus_handler(self):
        self.settings_buttons[self.cur_button - 1].plus()
    
    def minus_handler(self):
        self.settings_buttons[self.cur_button - 1].minus()

    def right_handler(self):
        self.settings_buttons[self.cur_button - 1].right()

    def handle_touch(self, x, y):
        if self.edit_mode:
            for i, button in enumerate(self.settings_buttons, 1):
                result = button.handle_touch(x, y)
                if result:
                    self.toggle_button_highlight(i)
                    return result
            for button in[self.config_string, self.ok_button, self.cancel_button]:
                result = button.handle_touch(x, y)
                if result: return result
        else:
            return self.change_button.handle_touch(x, y)

    def clear(self):
        self.edit_mode_off()
        self.is_draw = False
        self.config_string.clear()
        self.time_string.clear()
        self.date_string.clear()
        if self.edit_mode:
            self.ok_button.clear()
            self.cancel_button.clear()
        else:
            self.change_button.clear()
