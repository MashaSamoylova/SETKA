from label import EditableLable
from button import Button
from utils import colors


class Tab:
    def __init__(self, lcd):
        self.lcd = lcd
        self.status_error = False
        self.error_msg = ""
        self.error_button = Button(lcd, 0, 125, 128, 30, "")
        self.error_button.set_handler(self.notify_error)
        self.strings = [EditableLable(lcd, 45, y, "000.0", 100) for y in range(45, 106, 20)]

    def draw(self):
        for string in self.strings: string.draw()
        if self.status_error:
            self.draw_error()

    def handler(self):
        touch, x, y = self.lcd.get_touch()
        if touch:
            if self.status_error:
                if self.error_button.is_touched(x,y):
                    self.error_button.handler()

    def draw_error(self):
        self.error_button.draw(colors["black"], colors["red"])

    def notify_error(self):
        self.error_button.draw(colors["red"], colors["white"])
        self.error_button.clear_draw_button()
        self.status_error = False

