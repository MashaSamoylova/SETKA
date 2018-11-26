from editable_button import EditableButton
from button import Button
from utils import colors


class Tab1:
    """First tab, consists of 4 EditableButtons and a "Change" button"""

    edit_mode = False
    
    def __init__(self, lcd):
        self.extrudo_button = EditableButton(lcd, 45, 40, 128, 17, "000.0")
        self.first_head_button = EditableButton(lcd, 45, 58, 128, 17, "000.0")
        self.second_head_button = EditableButton(lcd, 45, 76, 128, 17, "000.0")
        self.acceptance_button = EditableButton(lcd, 45, 94, 128, 17, "000.0")

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
        return 1

    def ok_handler(self):
        print('OK')
        self.edit_mode = False
        return 1

    def cancel_handler(self):
        self.edit_mode = False
        return 1

    def handle_touch(self, x, y):
        if self.edit_mode:
            for button in [self.extrudo_button, self.first_head_button, 
                           self.second_head_button, self.acceptance_button,
                           self.ok_button, self.cancel_button]:
                result = button.handle_touch(x, y)
                if result: return result
        else:
            return self.change_button.handle_touch(x, y)

    def clear(self):
        self.extrudo_button.clear()
        self.first_head_button.clear()
        self.second_head_button.clear()
        self.acceptance_button.clear()
        if self.edit_mode:
            self.ok_button.clear()
            self.cancel_button.clear()
        else:
            self.change_button.clear()
