from ui.views import Button, Label
from ui.utils import colors
from pyb import Timer

class Tab2:
    """Second tab, consists of 4 Labels of temperature and pressuare"""

    is_draw = False

    def __init__(self, lcd, control):
        self.strings = [Label(lcd, 45, 30 + i * 25, "000.0",
                              fg=colors['green' if i // 2 else 'red']) for i in range(4)]
        self.update_timer = Timer(5)
        self.update_timer.callback(lambda t: self.on_tick())
        self.update_timer.init(freq=1)

    def on_tick(self):
        if self.is_draw and self.control.makhina.wip:
            self.update_data()

    def update_data(self):
        self.strings[0].text = control.t1
        self.strings[1].text = control.t2
        self.strings[2].text = control.p1
        self.strings[3].text = control.p2
        for string in self.strings:
            string.draw()

    def draw(self):
        self.is_draw = True
        self.update_data()
    
    def handle_touch(self, x, y):
        return 0

    def clear(self):
        self.is_draw = False
        for string in self.strings:
            string.clear()
