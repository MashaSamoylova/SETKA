import time

import lcd160cr
import pyb

from pyb import Pin
from pyb import Timer
from utils import colors

class Button:

    handler = lambda: 0

    def __init__(self, lcd, x, y, width, height, text):
        self.lcd = lcd
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.text_position_x = self.x + self.width // 2 - len(self.text)//2 - 5
        self.text_position_y = self.y + self.height // 2 - 5

    def draw(self, fg, bg):
        self.lcd.set_text_color(self.lcd.rgb(*fg), self.lcd.rgb(*bg))
        self.lcd.set_pen(self.lcd.rgb(*fg), self.lcd.rgb(*bg))
        self.lcd.rect(self.x, self.y, self.width, self.height)
        self.lcd.set_pos(self.text_position_x, self.text_position_y)
        self.lcd.set_font(1, scale=1, bold=0, trans=0, scroll=0)
        self.lcd.write(self.text)

    def draw_normal(self):
        self.draw(colors["white"], colors["black"])

    def draw_touched(self):
        self.draw(colors["black"], colors["white"])
        
    def clear(self):
        self.draw(colors["black"], colors["black"])

    def handle_touch(self, x, y):
        if x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height:
            self.draw_touched()
            time.sleep(0.3)
            return self.handler()
