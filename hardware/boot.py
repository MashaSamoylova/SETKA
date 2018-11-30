import lcd160cr
import micropython
import machine

from pyb import Pin
from pyb import Timer

from ui.screen import Screen
from makhina.makhina import Makhina


# set more detailed information on the exception
micropython.alloc_emergency_exception_buf(100)

# lcd
lcd = lcd160cr.LCD160CR('X')
lcd.set_orient(lcd160cr.PORTRAIT)
lcd.set_pen(lcd.rgb(255, 255, 255), lcd.rgb(0, 0, 0))
lcd.set_brightness(29)
lcd.erase()

# gui
main_screen = Screen(lcd)

makhina = Makhina()
