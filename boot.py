import lcd160cr
import micropython
import machine

from pyb import Pin
from pyb import Timer

from screen import Screen
from tab1 import Tab1


#set more detailed information on the exception
micropython.alloc_emergency_exception_buf(100)

#lcd
lcd = lcd160cr.LCD160CR('X')
lcd.set_orient(lcd160cr.PORTRAIT)
lcd.set_pen(lcd.rgb(255, 255, 255), lcd.rgb(0, 0, 0))
lcd.set_brightness(29)
lcd.erase()

#buttons
up_switch = machine.Pin("Y1", machine.Pin.IN, machine.Pin.PULL_UP)
down_switch = machine.Pin("Y2", machine.Pin.IN, machine.Pin.PULL_UP)
right_switch = machine.Pin("Y3", machine.Pin.IN, machine.Pin.PULL_UP)
start_switch = machine.Pin("Y4", machine.Pin.IN, machine.Pin.PULL_UP)
stop_switch = machine.Pin("Y5", machine.Pin.IN, machine.Pin.PULL_UP)

#gui
main_screen = Screen(lcd)
