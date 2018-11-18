import machine
import pyb
import math
import lcd160cr
from pyb import Pin
from pyb import Timer
from sm import SM
from button import Button
from label import Label

#создаем объект класса lcd160cr, с инициализация для пинов под подключение XY
lcd = lcd160cr.LCD160CR('XY')
#вертикальная отрисовка изображения
lcd.set_orient(lcd160cr.PORTRAIT)

#создаем объект класса SM, ШДЭ
sme = SM("SME", Timer(2), Pin('Y3', Pin.OUT), 5000, 3)
#создаем объект класса SM, ШДП1
smh1 = SM("SMH1", Timer(3), Pin('Y12', Pin.OUT), 18000, 4)
#создаем объект класса SM, ШДП2
smh2 = SM("SMH2", Timer(1), Pin('Y6', Pin.OUT), 18000, 1)
#создаем объект класса SM, ШДГ
smr = SM("SMR", Timer(4), Pin('X9', Pin.OUT), 3200, 1)
#объединяем объект класса SM в список
sm = [sme, smh1, smh2, smr]

#создаем объект класса Pin, пид для подания питания на шаговики: ШДЭ, ШДГ1, ШДГ2
enablePulse = Pin('Y5', Pin.OUT)
#создаем объект класса Pin, пид для подания питания на шаговики: ШДП
enablePulseReceiver = Pin('Y7', Pin.OUT)
#выставляем выдаваемое значение пином, логический ноль
enablePulse.low()
#выставляем выдаваемое значение пином, логический ноль
enablePulseReceiver.low()

#создаем объект класса Timer, ведущий таймер для выполненияв конкретный момент времени основной программы
timProcess = Timer(11, freq=10)
#флажок для разрешения выполнения программы
process = False
#основной счетчик
encounter = 0

#счетчик для дисплея, через какое время доступна проверка касания на дисплее
encounterTouch = 0
#флажок косания по дисплею
Touch = False
#позиция нажатия по дисплею по X
X = 0
#позиция нажатия по дисплею по Y
Y = 0

#список из одного элемента, для создания ссылки на изменяемый объект: Гц(int)
gz = [0]
#на сколько изменяется +- обороты в минуту(float)
factor = 10.0
#количество оборотов в минуту, список из одного элемента, для создания ссылки на изменяемый объекь: Об/мин(float)
roundPerMinut = [0] #float(gz[0] / (sme.con / 60))
#флажок для определения, изменяем в данный момент скорость вращения
change = False
#выбор шаговика, либо выбор режима инициализация
choice = 0

#кнопка старт
buttonOn = Pin('X12', Pin.IN, Pin.PULL_UP)
#кнопка стоп
buttonOff = Pin('X10', Pin.IN, Pin.PULL_UP)
#флажок для кнопки стоп
flag_stop = True
#флажок для кнопки старт
flag_start = True
#кнопка плюс
buttonPlus = Button(lcd, 98, 0, 30, 30, "+")
#кнопка минус
buttonMinus = Button(lcd, 98, 60, 30, 30, "-")
#кнопка сменить изменяемый символ
buttonShift = Button(lcd, 98, 30, 30, 30, ">>")
#кнопка поменять скорость
buttonChange = Button(lcd, 45, 120, 84, 41, "Change")
#кнопка принять значение
buttonOk = Button(lcd, 45, 120, 84, 41, "Ok")
#кнопка отменить изменение
buttonCancel = Button(lcd, -1, 120, 40, 40, "Cnl")
#кнопка выбора шаговика
buttonChoice = Button(lcd, 0, 0, 30, 30, "E")

#текст вывода Гц
labelGz = Label(lcd, 0, 90, gz)
#выключаем ограничение по тексту
labelGz.r = False
#текст вывода количество оборот в минуту
labelRPM = Label(lcd, 0, 60, "00.0")
#размер текста
labelRPM.s = 2
#дополнительное обозначение к тексту
labelRPM.e = "RPM"
