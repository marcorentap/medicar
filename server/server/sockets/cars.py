from server.app import socketio
import random
import time


car_statuses = {}
@socketio.on('set_car_status', namespace="/car_client")
def on_set_car_status(data):
    print(f"Received car status: {data}")
    car_statuses[data["id"]] = data

@socketio.on('get_car_statuses', namespace="/user_client")
def user_on_get_car_statuses(data):
    socketio.emit("car_statuses", car_statuses, namespace="/user_client")

@socketio.on('get_car_statuses', namespace="/car_client")
def car_on_get_car_statuses(data):
    socketio.emit("car_statuses", car_statuses, namespace="/car_client")

@socketio.on('car_make_measurement', namespace='user_client')
def on_car_make_measurement(data):
    # Data has id and measurement key
    print(data)