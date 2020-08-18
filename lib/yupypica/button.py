import asyncio
import gpiozero

class Button(object):
    __whenActiveCallback = None

    def __init__(self, pin, color, loop, whenActiveCallback):
        self.__whenActiveCallback = whenActiveCallback
        self.loop = loop
        self.color = color
        self.button = gpiozero.Button(pin)
        if self.button.is_active:
            raise(RuntimeError("%s button appears to be stuck" % color))

    def whenActive(self):
       # Create new asyncio loop
       asyncio.set_event_loop(self.loop)
       future = asyncio.ensure_future(self.__executeWhenActive())  # Execute async method

    async def __whenActive(self):
        await self.__whenActiveCallback()


class ButtonHandler(object):
    __whenButtonCallback = None

    def __init__(self, pin, color, whenButtonCallback):
        # whenButtonCallback is an async function
        self.__whenButtonCallback = whenButtonCallback
        self.color = color

        # Just init the sensor with gpiozero lib
        button = gpiozero.Button(pin)

        # Method to call when button is activated
        button.when_activated = self.whenButtonActive

    def whenButtonActive(self):
        # Create new asyncio loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(self.__executeWhenButtonCallback()) # Execute async method
        loop.run_until_complete(future)
        loop.close()

    async def __executeWhenButtonCallback(self):
        await self.__whenButtonCallback()
