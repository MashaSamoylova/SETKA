import machine
import pyb
import math
import lcd160cr
from pyb import Pin
from pyb import Timer

class Button:
 def __init__(self, lcd, xPos, yPos, width, height, text):
  self.l = lcd
  self.x = xPos
  self.y = yPos
  self.w = width
  self.h = height
  self.t = text
  self.scale = 1
  self.l.set_font(1, scale = self.scale, bold = 0, trans = 0, scroll = 0)
  self.text_position_x = self.x + self.w // 2 - int((len(self.t) / 2) * 12) #12
  self.text_position_y = self.y + self.h // 2 - 5 #5

 def draw(self, fg, bg):
  self.l.set_text_color(fg, bg)
  self.l.set_pen(fg, bg)
  self.l.rect(self.x, self.y, self.w, self.h)
  self.l.set_pos(self.text_position_x, self.text_position_y)
  self.l.write(self.t)

 def drawButton(self):
  self.draw(self.l.rgb(255, 0, 0), self.l.rgb(0, 0, 0))

 def touchDrawButton(self):
  self.draw(self.l.rgb(255, 0, 0), self.l.rgb(255, 255, 0))

 def clearDrawButton(self):
  self.draw(self.l.rgb(0, 0, 0), self.l.rgb(0, 0, 0))

 def setFunc(self, func):
  self.f = func
