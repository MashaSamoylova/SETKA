import uasyncio as asyncio
from ui.utils import zfill, chunkstring, to_float
import os

slave_addr=0x05

class Computer:

    connected = False

    def __init__(self, server, control, screen):
        self.server = server
        self.control = control
        self.screen = screen

    async def send_recipe(self, recipe):
        recipe = zfill(str(recipe), 3)
        print('sendrecipe', recipe)
        if recipe not in os.listdir('/sd/recipes'):
            speeds = [self.control.extrudo_speed,
                      self.control.first_head_speed,
                      self.control.second_head_speed,
                      self.control.reciever_speed]
        else:
            conf_val = open('/sd/recipes/' + recipe).read()
            speeds = chunkstring(conf_val, 5)
        to_send = ''.join(to_float(x) for x in speeds)
        print(to_send)
        success = False
        tries = 0
        if len(to_send) <= 1 or len(to_send) >= 123:
            await self.clear_command()
            return 
        while not success:
            try:
                success = await self.server.send_string(slave_addr, 
                                     50, to_send)
            except Exception as e:
                tries += 1
                if tries > 10:
                    raise e

    async def get_save_recipe(self, recipe):
        print('safe recipe')
        recipe_value = -1
        tries = 0
        while recipe_value == -1:
            try:
                recipe_value = await self.server.get_string(slave_addr, 50, 20)
            except Exception as e:
                tries += 1
                if tries > 10:
                    raise e
        print('recipe num is ', recipe)
        print('recipe_value is ', recipe_value)
        recipe_values = chunkstring(recipe_value, 5)
        recipe_values = ['{0:.1f}'.format(float(x)) for x in recipe_values]
        self.control.change_current_config(zfill(str(recipe), 3))
        self.control.set_speeds(recipe_values)
        self.screen.draw()
        print('recipe saved')

    async def send_sets_request(self):
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
        await asyncio.sleep_ms(10)
        res2 = await self.server.connection.write_single_register(slave_addr, 98, self.control.current_error + 1)
        return res and res2

    async def send_logs_list(self):
        if not os.listdir('/sd/logs'):
            gen = (ord(x) for x in 'no')
        else:
            gen = (ord(x) for y in os.listdir('/sd/logs') for x in y if x != '.')
        return await self.server.send_data(slave_addr, gen, 0)

    async def send_existing_configs(self):
        if not os.listdir('/sd/recipes'):
            gen = (ord(x) for x in 'no')
        else:
            gen = (ord(x) for y in os.listdir('/sd/recipes') for x in y if x != '.')
        return await self.server.send_data(slave_addr, gen, 0)

    async def send_log(self):
        log_name_raw = await self.server.get_string(slave_addr, 70, 10)
        log_name = '.'.join(chunkstring(log_name_raw, 2))
        print(log_name)
        if log_name not in os.listdir('/sd/logs'):
            print('NO LOG')
            return
        try:
            return await self.server.send_file(slave_addr, log_name)
        except Exception as e:
            print(e)
            return 0

    async def clear_command(self):
        await self.server.connection.write_single_register(slave_addr, 0x2, 0)
        #await self.server.connection.write_single_register(slave_addr, 0x3, 0)

    async def get_and_process_command(self):
        try:
            cmd = await self.server.connection.read_holding_registers(slave_addr, 0x2, 2, False)
            cmd, arg = cmd
        except Exception as e:
            print(e)
            if str(e) == 'no data received from slave':
                self.connected = False
        else:
            res = None
            try:
                if not cmd:
                    res = await self.send_sets_request()
                if cmd == 3:
                    res = await self.send_recipe(arg)
                if cmd == 4:
                    res = await self.get_save_recipe(arg)
                if cmd == 5:
                    res = await self.send_logs_list()
                if cmd == 6:
                    res = await self.send_log()
                if cmd == 7:
                    res = await self.send_existing_configs()
                if cmd and cmd not in [5, 6, 7]: await self.clear_command()
            except Exception as e:
                print('Exception while executing {cmd}th command:'.format(cmd=cmd), e)
            return res

    async def try_connect(self):
        try:
            return_flag = await self.server.connection.write_single_coil(slave_addr, 0x1, 0xFF00)
            print("return flag:", return_flag)
            if return_flag:
                await asyncio.sleep_ms(100)
                self.connected = True
        except Exception as e:
            print(e)
