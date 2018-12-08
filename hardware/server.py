from uModBus.serial import Serial
from mainconfig import uart_ctrl_pin

import uasyncio as asyncio
from pc import Computer
from makhina.makhina import Owen

class ModbusMaster:
    def __init__(self, control):
        self.connection = Serial(6, baudrate=115200, ctrl_pin=uart_ctrl_pin)
        self.pc = Computer(self, control)
        self.owen = Owen(self, control)
        loop = asyncio.get_event_loop()
        loop.create_task(self.serve())

    async def send_string(self, slave_addr, starting_address, text):
        try:
            return await self.connection.write_multiple_registers(slave_addr, starting_address, list(map(ord, text)))
        except Exception as e:
            print(e)

    async def get_string(self, slave_addr, starting_address, size):
        try:
            result = await self.connection.read_holding_registers(slave_addr, starting_address, size)
            print('result', result)
            return ''.join([chr(x) for x in result])
        except Exception as e:
            print(e)

    async def serve(self):
        while True:
            # Handle pc
            if self.pc.connected:
                await self.pc.get_and_process_command()
            else:
                await self.pc.try_connect()

            await asyncio.sleep_ms(50)
            # Handle owen
            await self.owen.read_owen_data()           
            await asyncio.sleep_ms(50)
