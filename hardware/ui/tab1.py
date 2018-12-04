from ui.views import Button, EditableButton
from ui.utils import colors


class Tab1:
    """First tab, consists of 4 EditableButtons and a "Change" button"""

    edit_mode = False
    cur_button = 0
    is_draw = True
    
    def __init__(self, lcd, makhina_control):
        self.makhina_control = makhina_control

        self.extrudo_button = EditableButton(lcd, 45, 30, 128, 20, "")
        self.first_head_button = EditableButton(lcd, 45, 55, 128, 20, "")
        self.second_head_button = EditableButton(lcd, 45, 80, 128, 20, "")
        self.acceptance_button = EditableButton(lcd, 45, 105, 128, 20, "")
        self.engines_buttons = [self.extrudo_button, self.first_head_button, 
                           self.second_head_button, self.acceptance_button]

        self.analog_buttons = [
     #           self.makhina_control.plus_button, 
                self.makhina_control.minus_button,
                self.makhina_control.right_button]

        self.change_button = Button(lcd, 0, 125, 128, 30, "Change")

        self.ok_button = Button(lcd, 0, 125, 64, 30, "Ok")
        self.cancel_button = Button(lcd, 64, 125, 64, 30, "Cnl")

        self.change_button.handler = self.change_handler
        self.ok_button.handler = self.ok_handler
        self.cancel_button.handler = self.cancel_handler

    def draw(self):
        self.extrudo_button.text =  self.makhina_control.extrudo_speed
        self.first_head_button.text = self.makhina_control.first_head_speed
        self.second_head_button.text = self.makhina_control.second_head_speed
        self.acceptance_button.text = self.makhina_control.reciever_speed

        self.extrudo_button.draw_normal()
        self.first_head_button.draw_normal()
        self.second_head_button.draw_normal()
        self.acceptance_button.draw_normal()

        if self.edit_mode:
            self.ok_button.draw_normal()
            self.cancel_button.draw_normal()
        else:
            self.change_button.draw_normal()
    
    def change_handler(self):
        self.edit_mode = True
        self.flash_edit(1)
    #    self.makhina_control.plus_button.handler = self.plus_handler
        self.makhina_control.minus_button.handler = self.minus_handler
        self.makhina_control.right_button.handler = self.right_handler
        return 1

    def ok_handler(self):
        print('OK')
        self.edit_mode = False
        self.off_flash_edit()
        self.makhina_control.set_speeds((x.text for x in self.engines_buttons))
    #    self.makhina_control.plus_button.handler = self.plus_handler = lambda: 1
        self.makhina_control.minus_button.handler = self.minus_handler = lambda: 1
        self.makhina_control.right_button.handler = self.right_handler = lambda: 1
        return 1

    def cancel_handler(self):
        self.edit_mode = False
        self.off_flash_edit()
        return 1

    def flash_edit(self, n):
        if self.cur_button:
            self.engines_buttons[self.cur_button - 1].edit_mode = False
            self.engines_buttons[self.cur_button - 1].draw_normal()
        if n == self.cur_button:
            self.cur_button = 0
        else:
            self.cur_button = n

    def off_flash_edit(self):
        if self.cur_button:
            self.engines_buttons[self.cur_button - 1].edit_mode = False
            self.engines_buttons[self.cur_button - 1].draw_normal()
        self.cur_button = 0

    def plus_handler(self):
        index = self.engines_buttons[self.cur_button - 1].char_editing
        string = self.engines_buttons[self.cur_button - 1].text
        digit = (int(string[index]) + 1)%10
        self.engines_buttons[self.cur_button - 1].text = string[:index] + str(digit) + string[index + 1:]
        self.engines_buttons[self.cur_button - 1].draw_normal()
    
    def minus_handler(self):
        index = self.engines_buttons[self.cur_button - 1].char_editing
        string = self.engines_buttons[self.cur_button - 1].text
        digit = (int(string[index]) - 1)%10
        self.engines_buttons[self.cur_button - 1].text = string[:index] + str(digit) + string[index + 1:]
        self.engines_buttons[self.cur_button - 1].draw_normal()

    def right_handler(self):
        self.engines_buttons[self.cur_button - 1].draw_normal()
        char_editing = self.engines_buttons[self.cur_button - 1].char_editing

        char_editing += 1
        char_editing %= len(self.engines_buttons[self.cur_button - 1].text)
        if self.engines_buttons[self.cur_button - 1].text[char_editing] == ".":
            char_editing += 1

        char_editing %= len(self.engines_buttons[self.cur_button - 1].text)
        self.engines_buttons[self.cur_button - 1].char_editing = char_editing

    def handle_touch(self, x, y):
        if self.edit_mode:
            for i, button in enumerate(self.engines_buttons, 1):
                result = button.handle_touch(x, y)
                if result:
                    self.flash_edit(i)
                    return result
            for button in [self.ok_button, self.cancel_button]:
                result = button.handle_touch(x, y)
                if result: return result

            for analog_button in self.analog_buttons:
                result = analog_button.handle_touch()
                if result: return result
        else:
            return self.change_button.handle_touch(x, y)

    def clear(self):
        self.off_flash_edit()
        self.edit_mode = False
        for i, button in enumerate(self.engines_buttons):
            button.clear()
        if self.edit_mode:
            self.ok_button.clear()
            self.cancel_button.clear()
        else:
            self.change_button.clear()
