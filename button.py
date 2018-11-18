import lcd160cr
import pyb

from pyb import Pin
from pyb import Timer


class Button:
    def __init__(self, lcd, x, y, width, height, text):
        self.lcd = lcd
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.text_position_x = self.x + self.width // 2 - len(self.text)//2 - 5
        self.text_position_y = self.y + self.height // 2 - 5

    def __draw(self, fg, bg):
        self.lcd.set_text_color(fg, bg)
        self.lcd.set_pen(fg, bg)
        self.lcd.rect(self.x, self.y, self.width, self.height)
        self.lcd.set_pos(self.text_position_x, self.text_position_y)
        self.lcd.set_font(1, scale=1, bold=0, trans=0, scroll=0)
        self.lcd.write(self.text)

    def draw(self):
        self.__draw(self.lcd.rgb(255, 255, 255), self.lcd.rgb(0, 0, 0))

    def draw_touched_button(self):
        self.__draw(self.lcd.rgb(0, 0, 0), self.lcd.rgb(255, 255, 255))
        
    def clear_draw_button(self):
        self.__draw(self.lcd.rgb(0, 0, 0), self.lcd.rgb(0, 0, 0))

    def is_touched(self, x, y):
        return x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height

    #redefine by child
    def handler():
        pass

    def set_handler(self, func):
        self.handler = func
