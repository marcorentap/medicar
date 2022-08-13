from time import sleep
import socketio
import json
import random

sio = socketio.Client()

def generate_random_loc():
    return {
        "data" : f"{random.randint(0,100)}, {random.randint(0,100)}",
        "sender" : "client"
    }

@sio.event
def connect():
    sio.emit("car_location", generate_random_loc())

@sio.on('server_response')
def emit_location(data):
    print(data)
    sio.emit("car_location", generate_random_loc())

@sio.event
def disconnect():
    print('disconnected from server')
    exit()

sio.connect('http://localhost:5000')
sio.wait()