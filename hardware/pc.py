import uasyncio as asyncio
from uModBus.serial import Serial
from mainconfig import uart_ctrl_pin
from ui.utils import zfill

slave_addr=0x05

class Computer:

    connected = False

    def __init__(self, control):
        self.connection = Serial(6, ctrl_pin=uart_ctrl_pin)
        self.control = control
        loop = asyncio.get_event_loop()
        loop.create_task(self.serve())

    def send_string(self, starting_address, text):
        #try:
        self.connection.write_multiple_registers(slave_addr, starting_address, list(map(ord, zfill(text, 5)[:5])))
        #except Exception as e:
        #    print(e)

    def send_sets_request(self):
        print('Sending sets')
        print(self.control.extrudo_speed)
        self.send_string(5, self.control.extrudo_speed)
        self.send_string(10, self.control.first_head_speed)
        self.send_string(15, self.control.second_head_speed)
        self.send_string(20, self.control.reciever_speed)
        self.send_string(25, self.control.config)

    def get_and_process_command(self):
        try:
            cmd = self.connection.read_holding_registers(slave_addr, 0x2, 1, False)[0]
        except Exception as e:
            if str(e) == 'no data received from slave':
                self.connected = False
        else:
            if cmd == 2:
                self.send_sets_request()

    async def serve(self):
        while True:
            if self.connected:
                self.get_and_process_command()
            else:
                try:
                    return_flag = self.connection.write_single_coil(slave_addr, 0x1, 0xFF00)
                    if return_flag:
                        self.connected = True
                except Exception as e:
                    print(e)
            await asyncio.sleep_ms(100)
