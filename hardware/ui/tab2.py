from ui.views import Button, Label
from ui.utils import colors

class Tab2:
    """Second tab, consists of 4 Labels of temperature and pressuare"""

    is_draw = False

    def __init__(self, lcd):
        self.strings = [Label(lcd, 45, 30 + i * 25, "000.0",
                              fg=colors['green' if i // 2 else 'red']) for i in range(4)]

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
