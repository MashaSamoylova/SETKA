import machine
import pyb
import math
import lcd160cr

class Label:
 def __init__(self, lcd, xPos, yPos, value):
  self.l = lcd
  self.x = xPos
  self.y = yPos
  self.v = value
  self.qt = 4
  self.r = True
  self.scale = 1
  self.l.set_font(1, scale = self.scale, bold = 0, trans = 0, scroll = 0)

 def drawChar(self, fg, bg, number):
  self.l.set_text_color(fg, bg)
  self.l.set_pos(self.x + number * 12, self.y)
  if type(self.v) == list:
   self.l.write(str(self.v[0])[number])
  else:
   self.l.write(str(self.v)[number])

 def draw(self, fg, bg):
  self.l.set_text_color(fg, bg)
  self.l.set_pos(self.x, self.y)
  if type(self.v) == list:
   self.l.write(str(self.v[0]))
  else:
   self.l.write(str(self.v))

 def drawLabel(self):
  self.draw(self.l.rgb(255, 0, 0), self.l.rgb(0, 0, 0))

 def drawFlash(self, number):
  value = 0
  if type(self.v) == list:
   value = self.v[0]
  else:
   value = self.v
  if (len(str(value)) - 1) >= number:
   self.drawChar(self.l.rgb(255, 255, 0), self.l.rgb(0, 0, 0), number)

 def clearDrawLabel(self):
  self.draw(self.l.rgb(0, 0, 0), self.l.rgb(0, 0, 0))

 def qtZeroDrawLabel(self):
  while(len( str(self.v)) < self.qt):
   self.v = "0" + str(self.v)
  if self.r:
   self.v = self.v[0:self.qt]
  self.draw(self.l.rgb(255, 0, 0), self.l.rgb(0, 0, 0))
