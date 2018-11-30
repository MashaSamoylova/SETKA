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
    
    def start(self):
        makhina.start()

    def stop(self):
        makhina.stop()

    def set_speeds(self, speeds):
        extrudo_speed, first_head_speed, second_head_speed, reciever_speed = speeds

        self.makhina.extrudo_engine.set_round_per_min(extrudo_speed)
        self.makhina.first_head_engine.set_round_per_min(first_head_speed)
        self.makhina.second_head_engine.set_round_per_min(second_head_speed)
        self.makhina.reciever_engine.set_round_per_min(reciever_speed)


class AnalogButton:

    handler = lambda: 0

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

