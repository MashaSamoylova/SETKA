from ui.views import Button, Label
from ui.utils import colors

class Tab2:
    """Second tab, consists of 4 Labels of temperature and pressuare"""

    is_draw = False

    def __init__(self, lcd):
        self.temperature1 = Label(lcd, 45, 30, "200.0", fg=colors["red"])
        self.temperature2 = Label(lcd, 45, 45, "000.0", fg=colors["red"])
        self.pressure1 = Label(lcd, 45, 60, "000.0", fg=colors["green"])
        self.pressure2 = Label(lcd, 45, 75, "000.0", fg=colors["green"])

        self.strings = [self.temperature1, self.temperature2, self.pressure1, self.pressure2]

    def draw(self):
        self.is_draw = True
        for string in self.strings:
            string.draw()
    
    def handle_touch(self, x, y):
        return 0

    def clear(self):
        self.is_draw = False
        for string in self.strings:
            string.clear()
