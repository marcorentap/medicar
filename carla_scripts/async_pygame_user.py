import glob
import os
import sys
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
import random
import pygame
import numpy as np
from agents.tools.misc import compute_distance
from medicar_simulator import create_user_carla
import asyncio
import requests


# Render object to keep and pass the PyGame surface
class RenderObject(object):
    def __init__(self, width, height):
        init_image = np.random.randint(0,255,(height,width,3),dtype='uint8')
        self.surface = pygame.surfarray.make_surface(init_image.swapaxes(0,1))

# Camera sensor callback, reshapes raw data from camera into 2D RGB and applies to PyGame surface
def pygame_callback(data, obj):
    img = np.reshape(np.copy(data.raw_data), (data.height, data.width, 4))
    img = img[:,:,:3]
    img = img[:, :, ::-1]
    obj.surface = pygame.surfarray.make_surface(img.swapaxes(0,1))

async def get_ego_user(world):
    spawn_points = world.get_map().get_spawn_points()
    blueprints = world.get_blueprint_library().filter("walker.pedestrian.*")
    ego_user = None
    for spawn_point in spawn_points: # Replace with better Medicar Stations later
        blueprint = random.choice(blueprints)
        ego_user = world.try_spawn_actor(blueprint, spawn_point)
        if ego_user is not None:
            break
    return ego_user

async def get_user_carla(world, id):
    ego_user = await get_ego_user(world)
    user_carla = await create_user_carla(ego_user, id)
    return user_carla

def game_loop(medicar_carla):
    # Connect to the client and retrieve the world object
    client = carla.Client('localhost', 2000)
    world = client.get_world()

    # Set up the simulator in synchronous mode
    settings = world.get_settings()
    settings.synchronous_mode = True # Enables synchronous mode
    settings.fixed_delta_seconds = 0.05
    settings.no_rendering_mode = True
    world.apply_settings(settings)

    # Set up the TM in synchronous mode
    traffic_manager = client.get_trafficmanager()
    traffic_manager.set_synchronous_mode(True)

    # Set a seed so behaviour can be repeated if necessary
    traffic_manager.set_random_device_seed(0)
    random.seed(0)

    # Initialise the camera floating behind the vehicle
    camera_init_trans = carla.Transform(carla.Location(x=-5, z=3), carla.Rotation(pitch=-20))
    camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
    camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=medicar_carla.actor)

    # Start camera with PyGame callback
    camera.listen(lambda image: pygame_callback(image, renderObject))

    # Get camera dimensions
    image_w = camera_bp.get_attribute("image_size_x").as_int()
    image_h = camera_bp.get_attribute("image_size_y").as_int()

    # Instantiate objects for rendering
    renderObject = RenderObject(image_w, image_h)

    # Initialise the display
    pygame.init()
    gameDisplay = pygame.display.set_mode((image_w,image_h), pygame.HWSURFACE | pygame.DOUBLEBUF)
    # Draw black to the display
    gameDisplay.fill((0,0,0))
    gameDisplay.blit(renderObject.surface, (0,0))
    pygame.display.flip()

    # Game loop
    crashed = False

    # async loop
    loop = asyncio.get_event_loop()
    loop.create_task(user_carla.user_client.create_session())
    frame_count = 0
    while not crashed:
        run_once(loop)

        frame_count += 1
        frame_count %= 10000
        # Every 60 frames
        if frame_count % 60 == 0:
            # Get car statuses
            loop.create_task(
                user_carla.user_client.get_car_statuses()
            )

        # Advance the simulation time
        world.tick()
        # Update the display
        gameDisplay.blit(renderObject.surface, (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            # If the window is closed, break the while loop
            if event.type == pygame.QUIT:
                crashed = True

    # Stop camera and quit PyGame after exiting game loop
    camera.stop()
    pygame.quit()
    loop.close()

def run_once(loop):
    loop.call_soon(loop.stop)
    loop.run_forever()

if __name__ == "__main__":
    user_id = sys.argv[1]
    client = carla.Client('localhost', 2000)
    world = client.get_world()
    loop = asyncio.get_event_loop()
    user_carla = loop.run_until_complete(get_user_carla(world, int(user_id)))
    game_loop(user_carla)