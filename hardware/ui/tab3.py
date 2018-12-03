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
    cur_button = 0
    
    def __init__(self, lcd, makhina_control):
        self.config_string = EditableButton(lcd, 75, 50, 128, 17, makhina_control.config)
        self.time_string = EditableButton(lcd, 30, 80, 128, 17, "")
        self.date_string = EditableButton(lcd, 5, 100, 128, 17, "")

        self.settings_buttons = [self.config_string, self.time_string, self.date_string]
        self.time_string.font_size = 1
        self.date_string.font_size = 1

        self.change_button = Button(lcd, 0, 125, 128, 30, "Change")

        self.ok_button = Button(lcd, 0, 125, 64, 30, "Ok")
        self.cancel_button = Button(lcd, 64, 125, 64, 30, "Cnl")

        self.change_button.handler = self.change_handler
        self.ok_button.handler = self.ok_handler1
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

    def ok_handler1(self):
        self.edit_mode = False
        self.off_flash_edit()
        self.makhina_control.plus_button.handler = self.plus_handler = lambda: 1
        self.makhina_control.minus_button.handler = self.minus_handler = lambda: 1
        self.makhina_control.right_button.handler = self.right_handler = lambda: 1

        print("CHANGED CONFIG", self.config_string.text)
        self.makhina_control.config = self.config_string.text
        self.makhina_control.change_current_config()
        self.off_flash_edit()
        return 1

    def flash_edit(self, n):
        print("cut =", self.cur_button, "n =", n)
        if self.cur_button:
            self.settings_buttons[self.cur_button - 1].edit_mode = False
            self.settings_buttons[self.cur_button - 1].draw_normal()
        if n == self.cur_button:
            self.cur_button = 0
        else:
            self.cur_button = n

    def off_flash_edit(self):
        if self.cur_button:
            self.settings_buttons[self.cur_button - 1].edit_mode = False
            self.settings_buttons[self.cur_button - 1].draw_normal()
        self.cur_button = 0

    def ok_handler(self):
        print('OK')
        self.edit_mode = False
        self.off_flash_edit()
        self.makhina_control.plus_button.handler = self.plus_handler = lambda: 1
        self.makhina_control.minus_button.handler = self.minus_handler = lambda: 1
        self.makhina_control.right_button.handler = self.right_handler = lambda: 1
        return 1

    def cancel_handler(self):
        self.edit_mode = False
        self.off_flash_edit()
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

    def plus_handler(self):
        index = self.settings_buttons[self.cur_button - 1].char_editing
        string = self.settings_buttons[self.cur_button - 1].text
        digit = (int(string[index]) + 1)%10
        self.settings_buttons[self.cur_button - 1].text = string[:index] + str(digit) + string[index + 1:]
        self.settings_buttons[self.cur_button - 1].draw_normal()

    def minus_handler(self):
        index = self.settings_buttons[self.cur_button - 1].char_editing
        string = self.settings_buttons[self.cur_button - 1].text
        digit = (int(string[index]) - 1)%10
        self.settings_buttons[self.cur_button - 1].text = string[:index] + str(digit) + string[index + 1:]
        self.settings_buttons[self.cur_button - 1].draw_normal()

    def right_handler(self):
        print("right handler")
        self.settings_buttons[self.cur_button - 1].draw_normal()
        char_editing = self.settings_buttons[self.cur_button - 1].char_editing
        char_editing += 1
        char_editing %= len(self.settings_buttons[self.cur_button - 1].text)
        if self.settings_buttons[self.cur_button - 1].text[char_editing] == ":":
            char_editing += 1

        char_editing %= len(self.settings_buttons[self.cur_button - 1].text)
        self.settings_buttons[self.cur_button - 1].char_editing = char_editing

    def handle_touch(self, x, y):
        if self.edit_mode:
            for i, button in enumerate(self.settings_buttons, 1):
                result = button.handle_touch(x, y)
                if result:
                    self.flash_edit(i)
                    return result
            for button in[self.config_string, self.ok_button, self.cancel_button]:
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
