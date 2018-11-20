from button import Button


def handler_tab1_button():
    return 1


def handler_tab2_button():
    return 2


def handler_tab3_button():
    return 3


class Screen:
    """ romw will write this"""
    current_tab_number = 0

    def __init__(self, lcd):
        self.lcd = lcd
        self.tab1_button = Button(lcd, 0, 0, 42, 40, "1")
        self.tab1_button.set_handler(handler_tab1_button)
        self.tab2_button = Button(lcd, 42, 0, 42, 40, "2")
        self.tab2_button.set_handler(handler_tab2_button)
        self.tab3_button = Button(lcd, 84, 0, 42, 40, "3")
        self.tab3_button.set_handler(handler_tab3_button)

    def draw(self):
        """Draw tab buttons"""

        for i, tab in enumerate([self.tab1_button, self.tab2_button, self.tab3_button]):
            if i == self.current_tab_number:
                tab.draw_touched_button()
            else:
                tab.draw()

    def handler(self):
        touch, x, y = self.lcd.get_touch()
        if touch:
            if self.tab1_button.is_touched(x,y):
                return self.tab1_button.handler()
            elif self.tab2_button.is_touched(x,y):
                return self.tab2_button.handler()
            elif self.tab3_button.is_touched(x,y):
                return self.tab3_button.handler()
        return self.current_tab_number
        
