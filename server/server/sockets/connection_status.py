from server.app import socketio

@socketio.on('connect', namespace="/")
def on_root_connect():
    print("/ client connected")

@socketio.on('disconnect', namespace="/")
def on_root_disconnect():
    print("/ client connected")

@socketio.on('connect', namespace="/user_client")
def on_user_connect():
    print("User client connected")

@socketio.on('disconnect', namespace="/user_client")
def on_user_disconnect():
    print(f"User client disconnected")

@socketio.on('connect', namespace="/car_client")
def on_car_connect():
    print("Car client connected")

@socketio.on('disconnect', namespace="/car_client")
def on_client_disconnect():
    print(f"Car client disconnected")
