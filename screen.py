from button import Button
from label import EditableLable

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
            if self.tab1_button.is_touched(x,y):
                return self.tab1_button.handler()
            elif self.tab2_button.is_touched(x,y):
                return self.tab2_button.handler()
            elif self.tab3_button.is_touched(x,y):
                return self.tab3_button.handler()
        return self.tab_number
        
