from button import Button
from label import EditableLable

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
        
        #4 strings that display engines speeds
        self.strings = [EditableLable(lcd, 45, y, "000.0", 100) for y in range(45, 106, 20)]

    def draw(self):
        """Draw tab buttons"""

        for i, tab in enumerate([self.tab1, self.tab2, self.tab3]):
            if i == self.tab_number:
                tab.draw_touched_button
            else:
                tab.draw()
        for string in self.strings: string.draw()

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
        
