from pkgutil import ImpImporter
from server.app import socketio
from server.schema import Session
from server.utils.database_tools import sessions_pre_jsonify

@socketio.on('get_new_sessions', namespace="/car_client")
def on_get_new_sessions(data):
    sessions = Session.query.filter_by(car_id=None)
    sessions = sessions_pre_jsonify(sessions)
    socketio.emit("new_sessions", sessions, namespace="/car_client")