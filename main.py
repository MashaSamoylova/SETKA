import time

def symbol_switcher(t):
    l.symbol_switcher()

if __name__=="__main__":
    active_screen = screen1
    active_screen.draw()
    while True:
        new_tab_number = active_screen.handler()
        if new_tab_number != tab_number:
            tab_number = new_tab_number
            if tab_number == 1:
                active_screen = screen1
            elif tab_number == 2:
                active_screen = screen2
            elif tab_number == 3:
                active_screen = screen3
            active_screen.draw()
        
        
   # l.draw_label()
   # t.callback(symbol_switcher)
   # time.sleep(5)
   # t.deinit()
   # l.stop_symbol_flash()
   # l.flashing_symbol_number = 1
   # t.init(freq=3)
   # t.callback(symbol_switcher)
    
