from ui.views import Button
from ui.tab1 import Tab1
from ui.tab2 import Tab2
from ui.tab3 import Tab3
from ui.utils import colors

import uasyncio as asyncio

import gc

class Screen:
    """Main screen"""

    current_tab_number = 0
    status_error = False
    current_error = -1
    error_msg = ""

    def __init__(self, lcd, makhina_control):
        self.lcd = lcd
        self.tab_buttons = [Button(lcd, 42 * i, 0, 42, 20, str(i + 1)) for i in range(3)]
        self.tab_buttons[0].handler = lambda: 1
        self.tab_buttons[1].handler = lambda: 2
        self.tab_buttons[2].handler = lambda: 3
        self.makhina_control = makhina_control
        print(gc.mem_free())
        self.tab1 = Tab1(lcd, makhina_control)
        self.tab2 = Tab2(lcd, makhina_control)
        self.tab3 = Tab3(lcd, makhina_control)
        self.tabs = [self.tab1, self.tab2, self.tab3]

        self.error_button = Button(lcd, 0, 125, 128, 30, "")
        self.error_button.text_position_x = 150
        self.error_button.text_position_y = 130
        self.error_button.handler = self.notify_error
        loop = asyncio.get_event_loop()
        loop.create_task(self.handle_lcd_touch())
        loop.create_task(self.check_errors())
        loop.create_task(self.skip_errors())
        loop.create_task(self.unset_notify_client())

    def draw(self):
        """Draw tab buttons, errors and current tab"""

        for i, tab_button in enumerate(self.tab_buttons):
            if i == self.current_tab_number:
                tab_button.draw_touched()
            else:
                tab_button.draw_normal()
        self.tabs[self.current_tab_number].draw()
        if self.status_error:
            self.draw_error()        

    async def handle_lcd_touch(self):
        while True:
            touch, x, y = self.lcd.get_touch()
            if touch: 
                result = self.handle_touch(x, y)
                if result:
                    self.draw()
                    await asyncio.sleep_ms(200)
            await asyncio.sleep_ms(50)

    def handle_touch(self, x, y):
        """Delegates touch handling to error_button,
           then to buttons and then to current tab"""

        if self.status_error and self.error_button.handle_touch(x,y): return 1
        for button in self.tab_buttons:
            result = button.handle_touch(x, y)
            if result: break
        if result and self.current_tab_number != result - 1:
                self.tabs[self.current_tab_number].clear()
                self.current_tab_number = result - 1
                return result
        else:
            return self.tabs[self.current_tab_number].handle_touch(x, y)

    async def check_errors(self):
        while True:
            for i in range(len(self.makhina_control.errors)):
                if not self.makhina_control.errors[i].active and self.makhina_control.errors[i].check():
                    self.makhina_control.errors[i].primary_handler()
                    self.makhina_control.errors[i].active = True
                    if self.current_error == -1:
                        self.set_status_error(self.makhina_control.errors[i].code)
                        self.draw()
                        self.current_error = i
                    print("[SCREEN] current_error", self.current_error)
                await asyncio.sleep_ms(100)
            await asyncio.sleep_ms(300)

    async def skip_errors(self):
        while True:
            for i in range(len(self.makhina_control.errors)):
                if self.makhina_control.errors[i].skip() and self.makhina_control.errors[i].active:
                    self.makhina_control.errors[i].active = False
                    print("[SCREEN] NEW CURRENT ERROR BEFORE SKIP", self.current_error)
                    self.current_error = self.get_next_error()
                    print("[SCREEN] NEW CURRENT ERROR AFTER SKIP", self.current_error)
                    if self.current_error == -1:
                        self.error_button.clear()
                        self.status_error = False
                    else:
                        self.set_status_error(self.makhina_control.errors[self.current_error].code)
                    self.draw()
                await asyncio.sleep_ms(100)
            await asyncio.sleep_ms(300)

    async def unset_notify_client(self):
        print("[SCREEN] unset notify error")
        while True:
            for e in self.makhina_control.errors:
                e.notify_client = False
            await asyncio.sleep_ms(1 * 10 * 1000)

    def get_next_error(self):
        for i in range(len(self.makhina_control.errors)):
            if self.makhina_control.errors[i].active:
                return i
        return -1

    def set_status_error(self, code):
        codes = {
                1 : "Перегрев",
                2 : "↑давление",
                3 : "↓ур.сырья",
                4 : "Обрыв.рук.",
                5 : "↑толщина.сетки",
                6 : "Останов",
                }
        self.makhina_control.current_error = code
        self.tab1.edit_mode_off()
        self.tab3.edit_mode_off()
        self.status_error = True
        self.error_button.text = codes[code]

    def draw_error(self):
        self.error_button.draw(colors["white"], colors["red"])

    def notify_error(self):
        self.error_button.draw(colors["red"], colors["white"])
        self.error_button.draw(colors["red"], colors["white"])
        print("current_error", self.current_error)
        self.makhina_control.errors[self.current_error].notify_client = True
        print("[SCREEN] current errors notify_client", self.current_error, self.makhina_control.errors[self.current_error].notify_client)
        return 1
