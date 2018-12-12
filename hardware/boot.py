import lcd160cr
import micropython
import machine
import os

from pyb import Pin
from pyb import Timer
from pyb import RTC
import uasyncio as asyncio

from mainconfig import lcd_pins
from ui.screen import Screen
from makhina.control import MakhinaControl
from server import ModbusMaster


# set more detailed information on the exception
micropython.alloc_emergency_exception_buf(100)

if 'logs' not in os.listdir('/sd'):
    os.mkdir('/sd/logs')
if 'recipes' not in os.listdir('/sd'):
    os.mkdir('/sd/recipes')

# lcd
lcd = lcd160cr.LCD160CR(lcd_pins)
lcd.set_orient(lcd160cr.PORTRAIT)
lcd.set_pen(lcd.rgb(255, 255, 255), lcd.rgb(0, 0, 0))
lcd.set_brightness(29)
lcd.erase()

# gui
makhina_control = MakhinaControl()
main_screen = Screen(lcd, makhina_control)
master = ModbusMaster(makhina_control)
