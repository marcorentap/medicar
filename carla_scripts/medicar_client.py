import asyncio
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

from time import sleep
import random
import socketio
import requests
import json
import carla
from math import inf

def location_to_tuple(location):
    return (location.x, location.y, location.z)

def string_to_location(location):
    nums = location[1:-1].split(",")
    nums = [float(num) for num in nums]
    return carla.Location(nums[0], nums[1], nums[2])

new_sessions = []
car_statuses = []
class Car_Socket_Namespace(socketio.AsyncClientNamespace):
    async def on_connect(self):
        print("Car socket connected")

    async def on_disconnect(self):
        print("Car socket disconnected")

    async def on_new_sessions(self, data):
        global new_sessions
        new_sessions = data
        return data

    async def on_car_statuses(self, data):
        global car_statuses
        car_statuses = data

class User_Socket_Namespace(socketio.AsyncClientNamespace):
    async def on_connect(self):
        print("User socket connected")

    async def on_disconnect(self):
        print("User socket disconnected")
    
    async def on_car_statuses(self, data):
        global car_statuses
        car_statuses = data

class Car_Client():
    def __init__(self, medicar_carla, api_root, sio):
        self.medicar_carla = medicar_carla
        self.api_root = api_root
        self.sio = sio
        self.available = True
        self.attached_session = None
        self.destination = None

    def get_car(self, id):
        car_properties = requests.get(f"{self.api_root}/cars/{id}")
        return car_properties.json()
    
    async def broadcast_car_status(self):
        await self.sio.emit("set_car_status", {
            "id" : self.medicar_carla.properties["id"],
            "available" : self.available,
            "location" : str(location_to_tuple(self.medicar_carla.actor.get_location()))
        })

    async def get_new_sessions(self):
        await self.sio.emit("get_new_sessions", "")

    async def get_car_statuses(self):
        global car_statuses
        await self.sio.emit("get_car_statuses", "")
    
    async def accept_new_session(self):
        global new_sessions
        global car_statuses

        for session in new_sessions:
            closest_id = None
            closest_distance = inf
            destination = string_to_location(session['location'])
            for car in car_statuses:
                location = string_to_location(
                    car_statuses[car]['location']
                )
                distance = destination.distance(location)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_id = car
                    print(f"Car {car} is closest to {destination}")
                    if int(closest_id) == int(self.medicar_carla.car_id):
                        break
            if int(closest_id) == int(self.medicar_carla.car_id):
                # Accept session, attach car to session
                json_data = {
                    "car_id" : self.medicar_carla.car_id,
                }
                self.attached_session = session
                self.destination = destination
                session = requests.post(f"{self.api_root}/sessions/{session['id']}/attach-car", json = json_data)
                print(f"Car {self.medicar_carla.car_id} attached to session {session.content}")
                self.available = False
                break
            


class User_Client():
    def __init__(self, user_carla, api_root, sio):
        self.user_carla = user_carla
        self.api_root = api_root
        self.sio = sio

    def get_user(self, id):
        user_properties = requests.get(f"{self.api_root}/users/{id}")
        return user_properties.json()
    
    async def create_session(self):
        json_data = {
            "user_id" : self.user_carla.user_id,
            "location" : str(location_to_tuple(self.user_carla.actor.get_location()))
        }
        session = requests.post(f"{self.api_root}/sessions", json = json_data)
        print(f"User {self.user_carla.user_id} created session {session.content}")

    async def get_car_statuses(self):
        global car_statuses
        await self.sio.emit("get_car_statuses", "")
