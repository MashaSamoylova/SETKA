#Подключение модуля machine
import machine
#Подключение модуля pyboard
import pyb
#Подключение модуля математики
import math
#Подключение модуля lcd160cr
import lcd160cr
#Подключение класса Pin из модуля pyb
from pyb import Pin
#Подключение класса Timer из модуля pyb
from pyb import Timer

#Класс кнопки: объект класса lcd160cr, позиция по Х, позиция по Y, ширина кнопки, высота кнопки, текст внутри кнопки
class Button:
 def __init__(self, lcd, xPos, yPos, width, height, text):
  #объект класса lcd160cr
  self.l = lcd
  #позиция по Х
  self.x = xPos
  #позиция по Y
  self.y = yPos
  #ширина кнопки
  self.w = width
  #высота кнопки
  self.h = height
  #текст внутри кнопки
  self.t = text
  #размер текста
  self.scale = 1
  #выставляем размер текста
  self.l.set_font(1, scale = self.scale, bold = 0, trans = 0, scroll = 0)
  #находим центр для текста по Х
  self.text_position_x = self.x + self.w // 2 - int((len(self.t) / 2) * 12)
  #находим центр для текста по Y
  self.text_position_y = self.y + self.h // 2 - 5

 #Отрисовка кнопки: цвет контура, цвет заполнения
 def draw(self, fg, bg):
  #задать цвет тексту
  self.l.set_text_color(fg, bg)
  #задать цвет для зарисовки квадрата
  self.l.set_pen(fg, bg)
  #нарисовать квадрат
  self.l.rect(self.x, self.y, self.w, self.h)
  #задать позицию для текста
  self.l.set_pos(self.text_position_x, self.text_position_y)
  #пишем текст для кнопки
  self.l.write(self.t)
 #Отрисовать кнопку
 def drawButton(self):
  self.draw(self.l.rgb(255, 0, 0), self.l.rgb(0, 0, 0))
 # Отрисовка кнопки после нажатия
 def touchDrawButton(self):
  self.draw(self.l.rgb(255, 0, 0), self.l.rgb(255, 255, 0))
 #Отисовки кнопки, закрасить в черный цвет
 def clearDrawButton(self):
  self.draw(self.l.rgb(0, 0, 0), self.l.rgb(0, 0, 0))
 #присвоить объекту кнопки объект функции
 def setFunc(self, func):
  self.f = func
