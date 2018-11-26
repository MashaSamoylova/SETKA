from views import Button, EditableButton, Label
from utils import colors


class Tab3:
    """Third tab, includes:
        blue string - sleeve width
        white editable string - config name
        white editable string - time
        white editable string - date"""

    edit_mode = False
    
    def __init__(self, lcd):
        self.sleeve_string = Label(lcd, 45, 40, "105")
        self.config_string = EditableButton(lcd, 45, 60, 128, 17, "001")
        self.time_string = EditableButton(lcd, 13, 79, 128, 17, "12:00:00")
        self.date_string = EditableButton(lcd, 13, 95, 128, 17, "31.12.18")
        self.time_string.font_size = 1
        self.date_string.font_size = 1

        self.change_button = Button(lcd, 0, 125, 128, 30, "Change")

        self.ok_button = Button(lcd, 0, 125, 64, 30, "Ok")
        self.cancel_button = Button(lcd, 64, 125, 64, 30, "Cnl")

        self.change_button.handler = self.change_handler
        self.ok_button.handler = self.ok_handler
        self.cancel_button.handler = self.cancel_handler

    def draw(self):
        self.sleeve_string.draw()
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
            for button in [self.time_string, self.date_string,
                           self.config_string, self.ok_button, self.cancel_button]:
                result = button.handle_touch(x, y)
                if result: return result
        else:
            return self.change_button.handle_touch(x, y)

    def clear(self):
        self.sleeve_string.clear()
        self.config_string.clear()
        self.time_string.clear()
        self.date_string.clear()
        if self.edit_mode:
            self.ok_button.clear()
            self.cancel_button.clear()
        else:
            self.change_button.clear()
