import lcd160cr
import pyb

from utils import colors


class Label:
    """Text label. Display text on the screen"""

    # font scaler
    font_size = 2
    
    def __init__(self, lcd, x, y, text, limit):
        """Create Label object, set class variables"""

        self.lcd = lcd
        self.x = x
        self.y = y
        self.text = text
        # limit for text slicing
        self.limit = limit

    def __draw(self, fg, bg):
        """Display self.text at (x, y) pixel of the screen
           with fg and bg (foreground, backgroung) as colors"""

        self.lcd.set_text_color(fg, bg)
        self.lcd.set_pos(self.x, self.y)
        self.lcd.set_font(1, scale=self.font_size, bold=0, trans=0, scroll=0)
        self.lcd.write(self.text)

    def draw_char(self, fg, bg, number):
        """Draw single character of text in fg, bg colors"""

        self.lcd.set_text_color(fg, bg)
        self.lcd.set_pos(self.x + number * ((1 + self.font_size) * 6), self.y)
        self.lcd.set_font(1, scale=self.font_size, bold=0, trans=0, scroll=0)
        self.lcd.write(self.text[number])

    def draw(self, fg=colors["white"], bg=colors["black"]):
        """Slice text and call __draw
           with black and white bg, fg"""

        self.text = self.text[:self.limit]
        self.__draw(self.lcd.rgb(*fg), self.lcd.rgb(*bg))

    def clear_draw_label(self, fg=colors["black"], bg=colors["black"]):
        """Fill text space with black pixels"""

        self.__draw(self.lcd.rgb(*fg), self.lcd.rgb(*bg))

        
class EditableLable(Label):
    """Label that provides some methods for visual representation of edditing,
       such as flashing"""

    symbol_switcher = False
    flashing_symbol_number = 0

    def symbol_switcher(self):
        """Switch char condition based on symbol_switcher flag"""

        fg = self.lcd.rgb(0,0,0)
        bg = self.lcd.rgb(255, 255, 255)
        if self.symbol_switcher: fg, bg = bg, fg
        self.draw_char(fg, bg, self.flashing_symbol_number)
        self.symbol_switch = not self.symbol_switch

    def stop_symbol_flash(self):
        """Restore initial state of char"""

        self.draw_char(self.lcd.rgb(255,255,255), self.lcd.rgb(0, 0, 0), self.flashing_symbol_number)
