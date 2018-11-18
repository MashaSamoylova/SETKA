import machine
import pyb
import math
from pyb import Pin
from pyb import Timer

#Класс Серво Мотора
class SM:
 #Конструктор класса Серво Мотора: ключевое имя объекта(str), таймер(Timer), пин генерации импульсов(Pin), константа количество импульсов для одного оборота(int), 
  #канал для ШИМа(int)
 def __init__(self, name, timer, pul, const, channel):
  #ключевое имя объекта
  self.n = name
  #таймер
  self.t = timer
  #пин генерации импульсов
  self.p = pul
  #логический ноль генерируемый пином
  self.p.low()
  #константа количество импульсов для одного оборота
  self.con = const
  #канал для ШИМа
  self.chan = channel
  #текущая частота срабаывания таймера
  self.gzOld = 0
  #будущая частота срабаывания таймера
  self.gzNew = 0
  #ширина импульса ШИМ
  self.pul_width = 9000

 #функция, получить количество оборот в минуту в int значении
 def iRoundPerMin(self):
  return int(self.gzOld / (self.con / 60))
 #функция, получить количество оборот в минуту в float значении
 def fRoundPerMin(self):
  return float(self.gzOld / (self.con / 60))
 #получить Гц при данном значении оборот в минуту для данного объекта: количество оборотов в минуту(float)
 def getRoundPerMin(self, rpm):
  #получить по формуле количество Гц
  gzNew = int(rpm * (self.con / 60))
  #Цикл для полного соотвествия Гц
  while rpm > (gzNew / (self.con / 60)):
   gzNew = gzNew + 1
  return gzNew
 #изменить будущую частоту срабатывания таймера через обороты в минуту: обороты в минуту(float)
 def setRoundPerMin(self, rpm):
  #получить по формуле количество Гц
  self.gzNew = int(rpm * (self.con / 60))
  #Цикл для полного соотвествия Гц
  while rpm > (self.gzNew / (self.con / 60)):
   self.gzNew = self.gzNew + 1
 #Ускорение, изменить текущую частоту
 def Accel(self):
  #Если текущая частота равна нулю и меньше будущей частоты
  if self.gzOld == 0 and self.gzNew > self.gzOld:
   #Инициализовать таймер, задать частоту
   self.t.init(freq=1)
   #Создать объект класса канал, для созднаия ШИМа
   ch = self.t.channel(self.chan, pyb.Timer.PWM, pin=self.p, pulse_width=self.pul_width)
  #Если будущая частота больше текущей частоты
  if self.gzNew > self.gzOld:
   #Формула по нахождению разницы для плавного разгона
   dif = math.sqrt(self.gzNew - self.gzOld) // 1
   #Изменяем текущую частоту
   self.gzOld = self.gzOld + int(dif)
   #Задать частоту для таймера
   self.t.freq(self.gzOld)
  else: 
   #Текущая частота равна будущей
   self.gzOld = self.gzNew
   #Если текущая частота равно 0, то убрать таймер, а вместе с ним ШИМ
   if self.gzOld == 0:
    self.t.deinit()
	#Иначе задать частоту для таймера
   else:
    self.t.freq(self.gzOld)
 #Остановить таймер и ШИМ
 def Stop(self):
  self.gzOld == 0
  self.t.deinit()
