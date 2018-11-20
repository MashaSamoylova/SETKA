from editable_button import EditableButton
from button import Button
from utils import colors
from tab import Tab

class Tab1(Tab):
    """"""
    edit_mode = False
    
    def __init__(self, lcd):
        super().__init__(lcd)

        self.extrudo_button = EditableButton(lcd, 45, 50, 128, 15, "000.0")
        self.first_head_button = EditableButton(lcd, 45, 65, 128, 15, "000.0")
        self.second_head_button = EditableButton(lcd, 45, 80, 128, 15, "000.0")
        self.acceptance_button = EditableButton(lcd, 45, 95, 128, 15, "000.0")

        self.change_button = Button(lcd, 0, 125, 128, 30, "Change")

        self.ok_button = Button(lcd, 0, 125, 64, 30, "Ok")
        self.cancel_button = Button(lcd, 64, 125, 64, 30, "Cnl")

    def __draw(self):
        self.extrudo_button.draw()
        self.first_head_button.draw()
        self.second_head_button.draw()
        self.acceptance_button.draw()

        if self.edit_mode:
            self.ok_button.draw()
            self.cancel_button.draw()
        else:
            self.change_button.draw()

    def draw(self):
        self.__draw()
        super().draw()

    def __handler(self, touch, x, y):
        if self.edit_mode:
            for button in [
                    self.extrudo_button, 
                    self.first_head_button, 
                    self.second_head_button, 
                    self.acceptance_button,

                    self.ok_button,
                    self.cancel_button,
                    ]:
                if button.is_touched():
                    button.handler()
        else:
            if change_button.is_touched():
                self.edit_mode = True

                self.ok_button.draw()
                self.cancel_button.draw()

