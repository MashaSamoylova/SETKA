from uModBus.serial import Serial
from mainconfig import uart_ctrl_pin

from math import ceil
import uasyncio as asyncio
from pc import Computer
from makhina.makhina import Owen
from ui.utils import chunkstring, file_iter

class ModbusMaster:

    buffer_start = 100
    buffer_len = 100
    sending_offset = -1
    sending_data = None
    sending_block = False
    data_len = 0

    def __init__(self, control):
        self.connection = Serial(6, baudrate=115200, ctrl_pin=uart_ctrl_pin)
        self.pc = Computer(self, control)
        self.owen = Owen(self, control)
        loop = asyncio.get_event_loop()
        loop.create_task(self.serve())

    async def proceed_sending(self):
        self.sending_block = True
        to_send = []
        try:
            for i in range(self.buffer_len):
                to_send.append(next(self.sending_data))
        except StopIteration:
            self.sending_offset = -1
            self.sending_data = None
            self.data_len = 0
        else:
            self.sending_offset += 1
        try:
            res1 = await self.connection.write_multiple_registers(5, self.buffer_start, to_send)
            print('res1', res1)
            recieve_flag = 2 if self.sending_offset == -1 else 1
            res2 = await self.connection.write_single_register(5, 99, recieve_flag)
            print('res2', res1)
        except Exception as e:
            print('proceed exception', e)
            return 0
        else:
            return res1 or res2
        finally:
            self.sending_block = False

    async def send_data(self, slave_addr, data):
        self.sending_data = iter(data)
        self.sending_offset = 0
        #self.data_len = ceil(len(self.send_data) / self.buffer_len)
        #return await self.connection.write_single_register(slave_addr, 4, self.data_len)

    async def send_file(self, slave_addr, filename):
        return await self.send_data(slave_addr, file_iter('/sd/logs/' + filename))

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
                if self.sending_offset > -1 and not self.sending_block:
                    flag = await self.connection.read_holding_registers(5, 99, 1, False)
                    flag = flag[0]
                    if flag == 0:
                        await self.proceed_sending()
                else:
                    await self.pc.get_and_process_command()
            else:
                await self.pc.try_connect()

            await asyncio.sleep_ms(50)
            # Handle owen
            await self.owen.read_owen_data()           
            await asyncio.sleep_ms(50)
