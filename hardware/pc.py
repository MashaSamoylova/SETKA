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

    async def send_string(self, starting_address, text):
        try:
            await self.connection.write_multiple_registers(slave_addr, starting_address, list(map(ord, text)))
        except Exception as e:
            print(e)

    async def send_sets_request(self):
        print('Sending sets')
        await self.send_string(5, "".join(zfill(x, 5) for x in [
            self.control.extrudo_speed, 
            self.control.first_head_speed, 
            self.control.second_head_speed, 
            self.control.reciever_speed]))
        print("end sending")

    async def clear_command(self):
        print("cleare_command")
        await self.connection.write_single_register(slave_addr, 0x2, 0)

    async def get_and_process_command(self):
        print("get_and_process_command")
        try:
            print("try")
            cmd = await self.connection.read_holding_registers(slave_addr, 0x2, 1, False)
            cmd = cmd[0]
            print("cmd:", cmd)
        except Exception as e:
            print(e)
            if str(e) == 'no data received from slave':
                self.connected = False
        else:
            if cmd == 2:
                await self.send_sets_request()
                await self.clear_command()
                

    async def serve(self):
        while True:
            print("serve")
            if self.connected:
                await self.get_and_process_command()
            else:
                try:
                    return_flag = await self.connection.write_single_coil(slave_addr, 0x1, 0xFF00)
                    print("return flag:", return_flag)
                    if return_flag:
                        self.connected = True
                except Exception as e:
                    print(e)
            await asyncio.sleep_ms(500)
