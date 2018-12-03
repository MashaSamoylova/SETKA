import machine

import uasyncio as asyncio

from makhina.makhina import Makhina

class MakhinaControl:
    def __init__(self):
        self.makhina = Makhina()
        
        self.plus_button = AnalogButton("Y1")
        self.minus_button = AnalogButton("Y2")
        self.right_button = AnalogButton("Y3")
        self.start_button = AnalogButton("Y4")
        self.stop_button = AnalogButton("Y5")

        self.start_button.handler = self.start
        self.stop_button.handler = self.stop

        # скорости в форме строки, чтобы не переводить из частоты обратно
        self.extrudo_speed = ""
        self.first_head_speed = ""
        self.second_head_speed = ""
        self.reciever_speed = ""

        self.config = "000"
        self.change_current_config()

    def start(self):
        makhina.start()

    def stop(self):
        makhina.stop()

    def set_speeds(self, speeds):
        self.extrudo_speed, self.first_head_speed, self.second_head_speed, self.reciever_speed = speeds

        self.makhina.extrudo_engine.set_round_per_min(float(self.extrudo_speed))
        self.makhina.first_head_engine.set_round_per_min(float(self.first_head_speed))
        self.makhina.second_head_engine.set_round_per_min(float(self.second_head_speed))
        self.makhina.reciever_engine.set_round_per_min(float(self.reciever_speed))

        with open("./recipes/" + self.config, "w") as f:
            f.write(";".join([self.extrudo_speed, self.first_head_speed, self.second_head_speed, self.reciever_speed]))
            print("writing at ./recipes/" + self.config)

    def change_current_config(self):
        print("current_config", self.config)
        try:
            with open("./recipes/" + self.config) as f:
                speeds = f.read()
        except:
            with open("./recipes/" + self.config, "w") as f:
                speeds = ";".join(["000.0", "0.0", "0.0", "0.0"])
                f.write(speeds)

        self.extrudo_speed, self.first_head_speed, self.second_head_speed, self.reciever_speed = speeds.split(";")


class AnalogButton:

    handler = lambda : 1

    def __init__(self, pin):
        self.button = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
        loop = asyncio.get_event_loop()
        loop.create_task(self.handle_touch())

    async def handle_touch(self):
        while True:
            await asyncio.sleep_ms(50)
            if not self.button.value():
                self.handler()
                await asyncio.sleep_ms(200)

