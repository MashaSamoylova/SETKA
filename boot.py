import pyb
import lcd160cr
import micropython

from pyb import Pin
from pyb import Timer

from screen import Screen


#set more detailed information on the exception
micropython.alloc_emergency_exception_buf(100)

lcd = lcd160cr.LCD160CR('X')
lcd.set_orient(lcd160cr.PORTRAIT)
lcd.set_pen(lcd.rgb(255,255,255), lcd.rgb(0,0,0))
lcd.set_brightness(29)
lcd.erase()

tab_number = 1
screen1 = Screen(lcd, 1)
screen2 = Screen(lcd, 2)
screen3 = Screen(lcd, 3)

