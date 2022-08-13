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
import socketio
from medicar_client import Car_Socket_Namespace, Car_Client, User_Socket_Namespace, User_Client


# Setup sockets
api_root = "http://localhost:5000/API"
socket_root = "http://localhost:5000"
carla_host = "localhost"
carla_port = 2000

sio = socketio.AsyncClient()
car_socket = None
user_socket = None

class Medicar_Carla():
    def __init__(self, actor, id):
        global car_socket
        self.car_id = id
        self.actor = actor
        self.available = True
        self.car_client = Car_Client(self, api_root, car_socket)
        self.properties = self.car_client.get_car(id)

class User_Carla():
    def __init__(self, actor, id):
        global user_socket
        self.user_id = id
        self.actor = actor
        self.user_client = User_Client(self, api_root, user_socket)
        self.properties = self.user_client.get_user(id)

async def create_medicar_carla(actor, id):
    global car_socket
    if car_socket is None:
        car_socket = Car_Socket_Namespace("/car_client")
        sio.register_namespace(car_socket)
        await sio.connect(socket_root)
    return Medicar_Carla(actor, id)

async def create_user_carla(actor, id):
    global user_socket
    if user_socket is None:
        user_socket = User_Socket_Namespace("/user_client")
        sio.register_namespace(user_socket)
        await sio.connect(socket_root)
    return User_Carla(actor, id)

def location_to_tuple(location):
    return (location.x, location.y, location.z)

def clear_world():
    # Connect to the client and retrieve the world object
    client = carla.Client(carla_host, carla_port)
    world = client.get_world()

    # Set up the simulator in synchronous mode
    settings = world.get_settings()
    settings.synchronous_mode = True # Enables synchronous mode
    settings.fixed_delta_seconds = 0.05
    settings.no_rendering_mode = True
    world.apply_settings(settings)

    car_actors = world.get_actors().filter("vehicle.*")
    user_actors = world.get_actors().filter("walker.pedestrian.*")
    sensor_actors = world.get_actors().filter("sensor.*")

    actors = [car_actors, user_actors, sensor_actors]
    for actor_group in actors:
        for actor in actor_group:
            print(f"Destroyed {actor}")
            actor.destroy()

if __name__ == "__main__":
    clear_world()