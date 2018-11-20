import lcd160cr
import micropython

from pyb import Pin
from pyb import Timer

from screen import Screen
from tab import Tab
from tab1 import Tab1


#set more detailed information on the exception
micropython.alloc_emergency_exception_buf(100)

lcd = lcd160cr.LCD160CR('X')
lcd.set_orient(lcd160cr.PORTRAIT)
lcd.set_pen(lcd.rgb(255,255,255), lcd.rgb(0,0,0))
lcd.set_brightness(29)
lcd.erase()

tab_number = 1
main_screen = Screen(lcd)
tab1 = Tab1(lcd)
tab2 = Tab(lcd)
tab3 = Tab(lcd)
