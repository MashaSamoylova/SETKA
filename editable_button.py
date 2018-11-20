from button import Button
from utils import colors


class EditableButton(Button):
    """"""    
    font_size = 2


    def __init__(self, lcd, x, y, width, height, text):
        super().__init__(lcd, x, y, width, height, text)
        self.text_position_x = self.x
        self.text_position_y = self.y


    def __draw(self, fg, bg):
        self.lcd.set_text_color(fg, bg)
        self.lcd.set_pen(fg, bg)
        self.lcd.set_pos(self.text_position_x, self.text_position_y)
        self.lcd.set_font(1, scale=self.font_size, bold=0, trans=0, scroll=0)
        self.lcd.write(self.text)
    
    def draw(self, fg=colors["white"], bg=colors["black"]):
        self.__draw(self.lcd.rgb(*fg), self.lcd.rgb(*bg))

    def draw_char(self, fg, bg, number):
        """Draw single character of text in fg, bg colors"""

        self.lcd.set_text_color(fg, bg)
        self.lcd.set_pos(self.text_position_x + number * ((1 + self.font_size) * 6), self.text_position_y)
        self.lcd.set_font(1, scale=self.font_size, bold=0, trans=0, scroll=0)
        self.lcd.write(self.text[number])



        
