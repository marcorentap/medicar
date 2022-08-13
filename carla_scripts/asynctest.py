import asyncio

async def short_coroutine():
    print("SHORT")

async def long_running_coroutine():
    await short_coroutine()
    print("ONE")
    await asyncio.sleep(10)
    print("TWO")
    await asyncio.sleep(10)
    print("THREE")
    await asyncio.sleep(10)
    print("FOUR")

async def third_coroutine():
    print("GROUCHO")
    await asyncio.sleep(0.1)
    print("HARPO")
    await asyncio.sleep(0.1)
    print("ZEPPO")
    await asyncio.sleep(0.1)
    print("KARL")
    await asyncio.sleep(0.1)

async def fourth_coroutine():
    print("ONE FISH")
    await asyncio.sleep(0.1)
    print("TWO FISH")
    await asyncio.sleep(0.1)
    print("RED FISH")
    await asyncio.sleep(0.1)
    print("BLUE FISH")
    await asyncio.sleep(0.1)

loop = asyncio.get_event_loop()
task = loop.create_task(long_running_coroutine())
task2 = loop.create_task(fourth_coroutine())

def run_once(loop):
    loop.call_soon(loop.stop)
    loop.run_forever()

while True:
    run_once(loop)
    if input("Press RETURN >")=="exit":
        break
loop.close()