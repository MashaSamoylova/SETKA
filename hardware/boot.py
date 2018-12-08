import lcd160cr
import micropython
import machine

from pyb import Pin
from pyb import Timer
import uasyncio as asyncio

from mainconfig import lcd_pins
from ui.screen import Screen
from makhina.control import MakhinaControl

current_error = -1

# set more detailed information on the exception
micropython.alloc_emergency_exception_buf(100)

# lcd
lcd = lcd160cr.LCD160CR(lcd_pins)
lcd.set_orient(lcd160cr.PORTRAIT)
lcd.set_pen(lcd.rgb(255, 255, 255), lcd.rgb(0, 0, 0))
lcd.set_brightness(29)
lcd.erase()

# gui
makhina_control = MakhinaControl()
main_screen = Screen(lcd, makhina_control)

loop = asyncio.get_event_loop()
