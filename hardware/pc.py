import uasyncio as asyncio
from ui.utils import zfill

slave_addr=0x05

class Computer:

    connected = False

    def __init__(self, server, control):
        self.server = server
        self.control = control

    async def send_recipe(self, recipe):
        print('sendrecipe', recipe)
        recipe = recipe - 1
        return await self.server.send_string(slave_addr, 
                                             50, "".join(zfill(x, 5) for x in [
                                             self.control.extrudo_speed, 
                                             self.control.first_head_speed, 
                                             self.control.second_head_speed, 
                                             self.control.reciever_speed]))

    async def get_save_recipe(self, recipe):
        print('safe recipe')
        recipe = recipe - 1
        recipe_value = await self.server.get_string(slave_addr, 50, 20)
        print('recipe num is ', recipe)
        print('recipe_value is ', recipe_value)
        recipe_values = [''.join(recipe_value[i*5:(i+1)*5]) for i in range(4)]
        recipe_values = ['{0:.1f}'.format(float(x)) for x in recipe_values]
        recipe_values[0] = zfill(5, recipe_values[0])
        recipe_values[1:] = [x[-3:] for x in recipe_values[1:]]
        print(recipe_values)
        self.control.change_current_config(zfill(str(recipe), 3))
        self.control.set_speeds(recipe_values)
        print('recipe saved')

    async def send_sets_request(self):
        print('Sending sets and data')
        res = await self.server.send_string(slave_addr, 5, "".join(zfill(x, 5) for x in [
            self.control.extrudo_speed, 
            self.control.first_head_speed, 
            self.control.second_head_speed, 
            self.control.reciever_speed,
            self.control.config,
            self.control.t1,
            self.control.t2,
            self.control.p1,
            self.control.p2]))
        print("end sending")
        return res

    async def clear_command(self):
        print("clear_command")
        await self.server.connection.write_single_register(slave_addr, 0x2, 0)
        await self.server.connection.write_single_register(slave_addr, 0x3, 0)

    async def get_and_process_command(self):
        try:
            cmd = await self.server.connection.read_holding_registers(slave_addr, 0x2, 2, False)
            cmd, arg = cmd
            print("cmd:", cmd, "arg:", arg)
        except Exception as e:
            print(e)
            if str(e) == 'no data received from slave':
                self.connected = False
        else:
            res = None
            if cmd: await self.clear_command()
            if not cmd:
                res = await self.send_sets_request()
            if cmd == 3 and arg:
                res = await self.send_recipe(arg)
            if cmd == 4 and arg:
                res = await self.get_save_recipe(arg)

    async def try_connect(self):
        try:
            return_flag = await self.server.connection.write_single_coil(slave_addr, 0x1, 0xFF00)
            print("return flag:", return_flag)
            if return_flag:
                await asyncio.sleep_ms(100)
                self.connected = True
        except Exception as e:
            print(e)
