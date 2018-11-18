from button import Button
from label import Label

def handler_tab1():
    return 1

def handler_tab2():
    return 2

def handler_tab3():
    return 3

class Screen:
    
    def __init__(self, lcd, init_tab_number):
        self.lcd = lcd
        self.tab_number = init_tab_number
        
        self.tab1 = Button(lcd, 0, 0, 42, 40, "1")
        self.tab1.set_handler(handler_tab1)
        self.tab2 = Button(lcd, 42, 0, 42, 40, "2")
        self.tab2.set_handler(handler_tab2)
        self.tab3 = Button(lcd, 84, 0, 42, 40, "3")
        self.tab3.set_handler(handler_tab3)
        
        self.string1 = Label(lcd, 45, 45, "000.0", 100)
        self.string2 = Label(lcd, 45, 65, "000.0", 100)
        self.string3 = Label(lcd, 45, 85, "000.0", 100)
        self.string4 = Label(lcd, 45, 105, "000.0", 100)

    def draw(self):
        if self.tab_number == 1:
            self.tab1.draw_touched_button()
            self.tab2.draw()
            self.tab3.draw()
        elif self.tab_number == 2:
            self.tab1.draw()
            self.tab2.draw_touched_button()
            self.tab3.draw()
        elif self.tab_number == 3:
            self.tab1.draw()
            self.tab2.draw()
            self.tab3.draw_touched_button()

        self.string1.draw()
        self.string2.draw()
        self.string3.draw()
        self.string4.draw()

    def handler(self):
        touch, x, y = self.lcd.get_touch()
        if touch:
            if self.tab1.is_touched(x,y):
                return self.tab1.handler()
            elif self.tab2.is_touched(x,y):
                return self.tab2.handler()
            elif self.tab3.is_touched(x,y):
                return self.tab3.handler()
        return self.tab_number
        
