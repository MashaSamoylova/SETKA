import lcd160cr
import pyb


class Label:
    def __init__(self, lcd, x, y, text, limit):
        self.lcd = lcd
        self.x = x
        self.y = y
        self.text = text
        self.limit = limit
        self.size = 2
        self.symbol_switch = False
        self.flashing_symbol_number = 0

    def draw_char(self, fg, bg, number):
        self.lcd.set_text_color(fg, bg)
        self.lcd.set_pos(self.x + number * ((1 + self.size) * 6), self.y)
        self.lcd.set_font(1, scale=self.size, bold=0, trans=0, scroll=0)
        self.lcd.write(self.text[number])

    def __draw__(self, fg, bg):
        self.lcd.set_text_color(fg, bg)
        self.lcd.set_pos(self.x, self.y)
        self.lcd.set_font(1, scale=2, bold=0, trans=0, scroll=0)
        self.lcd.write(self.text)

    def draw(self):
        self.text = self.text[:self.limit]
        self.__draw__(self.lcd.rgb(255, 255, 255), self.lcd.rgb(0, 0, 0))

    def clear_draw_label(self):
        self.__draw__(self.lcd.rgb(0, 0, 0), self.lcd.rgb(0, 0, 0))

    def symbol_switcher(self):
        if self.symbol_switch == True:
            self.draw_char(self.lcd.rgb(0,0,0), self.lcd.rgb(255, 255, 255), self.flashing_symbol_number)
            self.symbol_switch = False
        else:
            self.draw_char(self.lcd.rgb(255,255,255), self.lcd.rgb(0, 0, 0), self.flashing_symbol_number)
            self.symbol_switch = True

    def stop_symbol_flash(self):
        self.draw_char(self.lcd.rgb(255,255,255), self.lcd.rgb(0, 0, 0), self.flashing_symbol_number)
        

