from datetime import datetime
from flask import Blueprint, jsonify, request
from server.schema import Session, db
from server.utils.database_tools import list_remove_instance_state, remove_instance_state
import json

sessions_routes = Blueprint('sessions_routes', __name__)

@sessions_routes.route("/", strict_slashes=False)
def get_sessions():
    sessions = Session.query.all()
    for session in sessions:
        measure_dt = session.__dict__['measurement_time']
        session.__dict__['measurement_time'] = measure_dt.strftime("%Y-%m-%d %H:%M:%S KST")

    sessions = list_remove_instance_state(sessions)
    for session in sessions:
        session['measurement_data'] = json.loads(session['measurement_data'])
    return jsonify(sessions)

@sessions_routes.route("/", methods=["POST"], strict_slashes=False)
def create_session():
    session = Session(
        car_id = None,
        measurement_time = datetime.now(),
        measurement_data = "{}",
        diagnosis_data = "{}"
    )
    session.user_id = request.json.get("user_id")
    session.location = request.json.get("location")
    db.session.add(session)
    db.session.commit()
    return get_session(session_id=session.id)

@sessions_routes.route('/<session_id>')
def get_session(session_id):
    session = Session.query.filter_by(id=session_id).first()
    if(session is None):
        return {"msg" : "The session does not exist"}, 404
    else:
        measure_dt = session.__dict__['measurement_time']
        session.__dict__['measurement_time'] = measure_dt.strftime("%Y-%m-%d %H:%M:%S KST")
        session = remove_instance_state(session)
        session['measurement_data'] = json.loads(session['measurement_data'])
        return jsonify(session)
