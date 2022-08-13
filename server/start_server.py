from server.app import app, socketio
from server.sockets import *

if __name__ == "__main__":
    socketio.run(app, debug=True)