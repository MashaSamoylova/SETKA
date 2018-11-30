from ui.views import Button
from ui.tab1 import Tab1
from ui.tab2 import Tab2
from ui.tab3 import Tab3
from ui.utils import colors

class Screen:
    """Main screen"""

    current_tab_number = 0
    status_error = False
    error_msg = ""

    def __init__(self, lcd):
        self.lcd = lcd
        self.tab_buttons = [Button(lcd, 42 * i, 0, 42, 20, str(i + 1)) for i in range(3)]
        self.tab_buttons[0].handler = lambda: 1
        self.tab_buttons[1].handler = lambda: 2
        self.tab_buttons[2].handler = lambda: 3
        self.tabs = [Tab1(lcd), Tab2(lcd), Tab3(lcd)]
        self.error_button = Button(lcd, 0, 135, 128, 15, "")
        self.error_button.handler = self.notify_error

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

    def handle_touch(self, x, y):
        """Delegates touch handling to error_button,
           then to buttons and then to current tab"""

        if self.status_error:
            result = self.error_button.handle_touch(x,y)
            if result: return 1
        for button in self.tab_buttons:
            result = button.handle_touch(x, y)
            if result: break
        if result:
            if self.current_tab_number != result - 1:
                self.tabs[self.current_tab_number].clear()
                self.current_tab_number = result - 1
                return result
        else:
            return self.tabs[self.current_tab_number].handle_touch(x, y)

    def draw_error(self):
        self.error_button.draw(colors["black"], colors["red"])

    def notify_error(self):
        self.error_button.draw(colors["red"], colors["white"])
        self.error_button.clear()
        self.status_error = False
