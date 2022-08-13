import asyncio

from medicar_simulator import create_user_carla, sio

async def test_medicar():
    user = await create_user_carla(None, 1)
    await sio.wait()

asyncio.run(test_medicar())