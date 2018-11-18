from button import Button
from label import Label

def handler_tab1_button():
    return 1

def handler_tab2_button():
    return 2

def handler_tab3_button():
    return 3

class Screen:
    
    def __init__(self, lcd, init_tab_number):
        self.lcd = lcd
        self.tab_number = init_tab_number
        
        self.tab1_button = Button(lcd, 0, 0, 42, 40, "1")
        self.tab1_button.set_handler(handler_tab1_button)
        self.tab2_button = Button(lcd, 42, 0, 42, 40, "2")
        self.tab2_button.set_handler(handler_tab2_button)
        self.tab3_button = Button(lcd, 84, 0, 42, 40, "3")
        self.tab3_button.set_handler(handler_tab3_button)
        
        self.string1 = Label(lcd, 45, 45, "000.0", 100)
        self.string2 = Label(lcd, 45, 65, "000.0", 100)
        self.string3 = Label(lcd, 45, 85, "000.0", 100)
        self.string4 = Label(lcd, 45, 105, "000.0", 100)

    def draw(self):
        if self.tab_number == 1:
            self.tab1_button.draw_touched_button()
            self.tab2_button.draw()
            self.tab3_button.draw()
        elif self.tab_number == 2:
            self.tab1_button.draw()
            self.tab2_button.draw_touched_button()
            self.tab3_button.draw()
        elif self.tab_number == 3:
            self.tab1_button.draw()
            self.tab2_button.draw()
            self.tab3_button.draw_touched_button()

        self.string1.draw()
        self.string2.draw()
        self.string3.draw()
        self.string4.draw()

    def handler(self):
        touch, x, y = self.lcd.get_touch()
        if touch:
            if self.tab1_button.is_touched(x,y):
                return self.tab1_button.handler()
            elif self.tab2_button.is_touched(x,y):
                return self.tab2_button.handler()
            elif self.tab3_button.is_touched(x,y):
                return self.tab3_button.handler()
        return self.tab_number
        
