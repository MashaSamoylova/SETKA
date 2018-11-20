from label import EditableLable
from button import Button
from utils import colors


class Tab:
    """"""
    status_error = False

    def __init__(self, lcd):
        self.lcd = lcd
        self.error_msg = ""
        self.error_button = Button(lcd, 0, 125, 128, 30, "")
        self.error_button.set_handler(self.notify_error)

    def __draw(self):
        pass

    def draw(self):
        self.__draw()
        if self.status_error:
            self.draw_error()        

        
    def __handler(self, touch, x, y):
        pass

    def handler(self):
        touch, x, y = self.lcd.get_touch()
        if touch:
            if self.status_error:
                if self.error_button.is_touched(x,y):
                    self.error_button.handler()
            else:
                self.__handler(touch, x, y)

    def draw_error(self):
        self.error_button.draw(colors["black"], colors["red"])

    def notify_error(self):
        self.error_button.draw(colors["red"], colors["white"])
        self.error_button.clear_draw_button()
        self.status_error = False

