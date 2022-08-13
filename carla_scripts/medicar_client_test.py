import asyncio

from medicar_simulator import create_medicar_carla, create_user_carla, sio
import random

# user = User_Carla(None, 1)
async def test_medicar():
    medicar = await create_medicar_carla(None, 1)
    for i in range(0, 100):
        await medicar.car_client.sio_set_car_location(f"{random.randint(0, 100)}")
    await sio.wait()
asyncio.run(test_medicar())
