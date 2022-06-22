import asyncio

async def every(__seconds: float, func, *args, **kwargs):
    while True:
        func(*args, **kwargs)
        await asyncio.sleep(__seconds)

a = asyncio.get_event_loop()
a.create_task(every(1, print, "Hello World"))
