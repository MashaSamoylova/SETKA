import machine
import pyb
import math
import lcd160cr
from pyb import Pin
from pyb import Timer
from sm import SM
from button import Button
from label import Label

lcd = lcd160cr.LCD160CR('X')
lcd.set_orient(lcd160cr.PORTRAIT)

sme = SM("SME", Timer(2), Pin('X3', Pin.OUT), 4000, 1)

timProcess = Timer(11, freq=10)
process = False
encounter = 0

encounterTouch = 0
Touch = False
X = 0
Y = 0

gz = [0]
factor = 10.0
roundPerMinut = [0]
change = False

buttonPlus = Button(lcd, 98, 0, 30, 30, "+")
buttonMinus = Button(lcd, 98, 60, 30, 30, "-")
buttonShift = Button(lcd, 98, 30, 30, 30, ">>")
buttonChange = Button(lcd, 45, 120, 84, 41, "Change")
buttonOk = Button(lcd, 45, 120, 84, 41, "Ok")
buttonCancel = Button(lcd, -1, 120, 40, 40, "Cnl")

labelGz = Label(lcd, 0, 90, gz)
labelGz.r = False
labelRPM = Label(lcd, 0, 60, "00.0")