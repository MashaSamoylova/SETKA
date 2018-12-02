from ui.views import Button, Label
from ui.utils import colors

class Tab2:
    is_draw = False
    """Second tab, consists of 4 Labels of temperature and pressuare"""

    def __init__(self, lcd):
        self.strings = [Label(lcd, 45, 40 + i * 18, "000.0",
                              fg=colors['green' if i // 2 else 'red']) for i in range(4)]

    def draw(self):
        for string in self.strings:
            string.draw()
    
    def handle_touch(self, x, y):
        return 0

    def clear(self):
        for string in self.strings:
            string.clear()
