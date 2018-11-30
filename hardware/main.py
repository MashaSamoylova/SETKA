import time

import uasyncio as asyncio


async def handle_lcd_touch():
    while True:
        touch, x, y = lcd.get_touch()
        if touch: 
            result = main_screen.handle_touch(x, y)
            if result:
                main_screen.draw()
                await asyncio.sleep_ms(200)
        await asyncio.sleep_ms(50)


if __name__=="__main__":
    main_screen.draw()
    loop = asyncio.get_event_loop()
    loop.create_task(handle_lcd_touch())
    loop.run_forever()
