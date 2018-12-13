import uasyncio as asyncio

if __name__=="__main__":
#    makhina_control.start()
    main_screen.draw()
    loop = asyncio.get_event_loop()
    loop.run_forever()
