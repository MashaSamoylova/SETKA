from ui.views import Button, EditableButton
from ui.utils import colors


class Tab1:
    """First tab, consists of 4 EditableButtons and a "Change" button"""

    edit_mode = False
    cur_button = 0
    
    def __init__(self, lcd):
        self.extrudo_button = EditableButton(lcd, 45, 30, 128, 20, "000.0")
        self.first_head_button = EditableButton(lcd, 45, 55, 128, 20, "000.0")
        self.second_head_button = EditableButton(lcd, 45, 80, 128, 20, "000.0")
        self.acceptance_button = EditableButton(lcd, 45, 105, 128, 20, "000.0")
        self.engines_buttons = [self.extrudo_button, self.first_head_button, 
                           self.second_head_button, self.acceptance_button]

        self.change_button = Button(lcd, 0, 125, 128, 30, "Change")

        self.ok_button = Button(lcd, 0, 125, 64, 30, "Ok")
        self.cancel_button = Button(lcd, 64, 125, 64, 30, "Cnl")

        self.change_button.handler = self.change_handler
        self.ok_button.handler = self.ok_handler
        self.cancel_button.handler = self.cancel_handler

    def draw(self):
        self.extrudo_button.draw_normal()
        self.first_head_button.draw_normal()
        self.second_head_button.draw_normal()
        self.acceptance_button.draw_normal()

        if self.edit_mode:
            self.ok_button.draw_normal()
            self.cancel_button.draw_normal()
        else:
            self.change_button.draw_normal()
    
    def change_handler(self):
        self.edit_mode = True
        self.flash_edit(1)
        return 1

    def ok_handler(self):
        print('OK')
        self.edit_mode = False
        self.off_flash_edit()
        return 1

    def cancel_handler(self):
        self.edit_mode = False
        self.off_flash_edit()
        return 1

    def flash_edit(self, n):
        if self.cur_button:
            self.engines_buttons[self.cur_button - 1].edit_mode = False
            self.engines_buttons[self.cur_button - 1].draw_normal()
        if n == self.cur_button:
            self.cur_button = 0
        else:
            self.cur_button = n

    def off_flash_edit(self):
        if self.cur_button:
            self.engines_buttons[self.cur_button - 1].edit_mode = False
            self.engines_buttons[self.cur_button - 1].draw_normal()
        self.cur_button = 0

    def handle_touch(self, x, y):
        if self.edit_mode:
            for i, button in enumerate(self.engines_buttons, 1):
                result = button.handle_touch(x, y)
                if result:
                    self.flash_edit(i)
                    return result
            for button in [self.ok_button, self.cancel_button]:
                result = button.handle_touch(x, y)
                if result: return result
        else:
            return self.change_button.handle_touch(x, y)

    def clear(self):
        self.off_flash_edit()
        self.edit_mode = False
        for i, button in enumerate(self.engines_buttons):
            button.clear()
        if self.edit_mode:
            self.ok_button.clear()
            self.cancel_button.clear()
        else:
            self.change_button.clear()
