#Подключение модуля machine
import machine
#Подключение модуля pyboard
import pyb
#Подключение модуля математики
import math
#Подключение модуля lcd160cr
import lcd160cr

#Класс этикетка: объект класса lcd160cr, позиция по X, позиция по Y, значение либо текст
class Label:
 def __init__(self, lcd, xPos, yPos, value):
  #объект класса lcd160cr
  self.l = lcd
  #позиция по X
  self.x = xPos
  #позиция по Y
  self.y = yPos
  #значение либо текст
  self.v = value
  #ограницение по символам, 4 символа
  self.qt = 4
  #применить ограничение
  self.r = True
  #размер текста
  self.s = 1
  #дополнительное слово, для обозначения значения
  self.e = ""
  #размер текста
  self.scale = 1
  #назначить размер текста
  self.l.set_font(1, scale = self.scale, bold = 0, trans = 0, scroll = 0)

 #Отрисовка конкретного символа: цвет контура, цвет заливки, номер символа
 def drawChar(self, fg, bg, number):
  #задать цвет текста
  self.l.set_text_color(fg, bg)
  #задать позицию для текста
  self.l.set_pos(self.x + number * ((1 + self.s) * 6), self.y)
  #задать размер
  self.l.set_font(1, scale=self.s, bold=0, trans=0, scroll=0)
  #если тип значения список
  if type(self.v) == list:
   #вывести значение
   self.l.write(str(self.v[0])[number])
  else:
   #написать текст
   self.l.write(str(self.v)[number])
  #вернуть стандартный размер текста
  self.l.set_font(1, scale=1, bold=0, trans=0, scroll=0)
 #Отрисовка: цвет контура, цвет заливки
 def draw(self, fg, bg):
  #задать цвет текста
  self.l.set_text_color(fg, bg)
  #задать позицию
  self.l.set_pos(self.x, self.y)
  #задать размер текста
  self.l.set_font(1, scale=self.s, bold=0, trans=0, scroll=0)
  #если тип значения список
  if type(self.v) == list:
   #написать значение
   self.l.write(str(self.v[0]))
  else:
   #написать текст
   self.l.write(str(self.v))
  #задать размер
  self.l.set_font(1)
  #написать дополнительное обозначение
  self.l.write(str(self.e))
  #вернуть стандрартный размер
  self.l.set_font(1, scale=1, bold=0, trans=0, scroll=0)
 #Отрисовать этикетки
 def drawLabel(self):
  self.draw(self.l.rgb(255, 0, 0), self.l.rgb(0, 0, 0))
 #Отрисовать выбранный символ: номер символа
 def drawFlash(self, number):
  #локальная переменая значения
  value = 0
  #если тип значение список
  if type(self.v) == list:
   #локальная переменая присваивает значение
   value = self.v[0]
  else:
   #локальная переменая присваивает значение текст
   value = self.v
  #если длина в символах значения больше или равна номеру символа
  if (len(str(value)) - 1) >= number:
  #отрисовать другим цветом символ
   self.drawChar(self.l.rgb(255, 255, 0), self.l.rgb(0, 0, 0), number)
 #Отрисовка этикетки, закрасить в черный цвет
 def clearDrawLabel(self):
  self.draw(self.l.rgb(0, 0, 0), self.l.rgb(0, 0, 0))
 #Дополнить текст до заданного ограничения
 def qtZeroDrawLabel(self):
  #пока длина строки меньше заданного ограничения по символам
  while(len( str(self.v)) < self.qt):
   #добавлять первый символ
   self.v = "0" + str(self.v)
  #если включено ограничение по символам
  if self.r:
   #вырезать первые 4 символа и присвоить их значению
   self.v = self.v[0:4]#self.qt вместо 4
  #отрисовать
  self.draw(self.l.rgb(255, 0, 0), self.l.rgb(0, 0, 0))
