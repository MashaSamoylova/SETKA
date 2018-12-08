from ui.views import Button, Label
from ui.utils import colors, to_float
import uasyncio as asyncio

class Tab2:
    """Second tab, consists of 4 Labels of temperature and pressuare"""

    is_draw = False

    def __init__(self, lcd, control):
        self.control = control
        self.strings = [Label(lcd, 45, 30 + i * 25, "000.0",
                              fg=colors['green' if i // 2 else 'red']) for i in range(4)]
        loop = asyncio.get_event_loop()
        loop.create_task(self.on_tick())

    async def on_tick(self):
        while True:
            if self.is_draw and self.control.makhina.wip:
                self.update_data()
            await asyncio.sleep_ms(1000)

    def update_data(self):
        self.strings[0].text = to_float(self.control.t1)
        self.strings[1].text = to_float(self.control.t2)
        self.strings[2].text = to_float(self.control.p1)
        self.strings[3].text = to_float(self.control.p2)
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
