from pyb import RTC

import uasyncio as asyncio

from ui.views import Button, EditableButton, Label
from ui.utils import colors


class Tab3:
    """Third tab, includes:
        white editable string - config name
        white editable string - time
        white editable string - date"""

    edit_mode = False
    is_draw = False
    
    def __init__(self, lcd, makhina_control):
        self.config_string = EditableButton(lcd, 75, 50, 128, 17, "001")
        self.time_string = EditableButton(lcd, 30, 80, 128, 17, "")
        self.date_string = EditableButton(lcd, 5, 100, 128, 17, "")
        self.time_string.font_size = 1
        self.date_string.font_size = 1

        self.change_button = Button(lcd, 0, 125, 128, 30, "Change")

        self.ok_button = Button(lcd, 0, 125, 64, 30, "Ok")
        self.cancel_button = Button(lcd, 64, 125, 64, 30, "Cnl")

        self.change_button.handler = self.change_handler
        self.ok_button.handler = self.ok_handler
        self.cancel_button.handler = self.cancel_handler

        self.rtc = RTC()
        self.update_time()
        loop = asyncio.get_event_loop()
        loop.create_task(self.timer())

        self.makhina_control = makhina_control

    def draw(self):
        self.config_string.draw_normal()
        self.time_string.draw_normal()
        self.date_string.draw_normal()
        if self.edit_mode:
            self.ok_button.draw_normal()
            self.cancel_button.draw_normal()
        else:
            self.change_button.draw_normal()
    
    def change_handler(self):
        self.edit_mode = True
        self.makhina_control.plus_button.handler = self.plus_handler
        self.makhina_control.minus_button.handler = self.minus_handler
        self.makhina_control.right_button.handler = self.right_handler
        return 1

    def ok_handler(self):
        print('OK')
        self.edit_mode = False
        return 1

    def cancel_handler(self):
        self.edit_mode = False
        return 1
    
    async def timer(self):
        while True:
            self.update_time()
            await asyncio.sleep_ms(1000)

    def update_time(self):
        if not self.edit_mode and self.is_draw:
            year, month, date, _, hour, minute, second, _ = self.rtc.datetime()
            self.time_string.text = ":".join(
                    [
                        "0"*(2 - len(str(hour))) + str(hour), 
                        "0"*(2 - len(str(minute))) + str(minute), 
                        "0"*(2 - len(str(second))) + str(second),
                        ])
            self.time_string.clear()
            self.time_string.draw_normal()
            
            new_date = ":".join(
            [
                str(year), 
                "0"*(2 - len(str(month))) + str(month), 
                "0"*(2 - len(str(date))) + str(date),
                ])

            if self.date_string.text != new_date:
                self.date_string.text = new_date
                self.time_string.clear()
                self.date_string.draw_normal()


    def handle_touch(self, x, y):
        if self.edit_mode:
            for button in [self.time_string, self.date_string,
                           self.config_string, self.ok_button, self.cancel_button]:
                result = button.handle_touch(x, y)
                if result: return result
        else:
            return self.change_button.handle_touch(x, y)

    def clear(self):
        self.config_string.clear()
        self.time_string.clear()
        self.date_string.clear()
        if self.edit_mode:
            self.ok_button.clear()
            self.cancel_button.clear()
        else:
            self.change_button.clear()
