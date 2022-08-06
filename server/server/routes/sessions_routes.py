from datetime import datetime
from flask import Blueprint, jsonify, request
from server.schema import Session, db, User
from server.utils.database_tools import list_remove_instance_state, remove_instance_state
import json

sessions_routes = Blueprint('sessions_routes', __name__)

def session_dict_get_kst(session_dict, time):
    if(session_dict[time] is not None):
        return session_dict[time].strftime("%Y-%m-%d %H:%M:%S KST")
    return ""

@sessions_routes.route("/", strict_slashes=False)
def get_sessions():
    sessions = Session.query.all()
    sessions = list_remove_instance_state(sessions)

    for session in sessions:
        session['measurement_data'] = json.loads(session['measurement_data'])
        session['diagnosis_data'] = json.loads(session['diagnosis_data'])
        session['measurement_time'] = session_dict_get_kst(session, 'measurement_time')
        session['diagnosis_time'] = session_dict_get_kst(session, 'diagnosis_time')
        session['time'] = session_dict_get_kst(session, 'time')
    return jsonify(sessions)

@sessions_routes.route("/", methods=["POST"], strict_slashes=False)
def create_session():
    session = Session(
        car_id = None,
        time = datetime.now(),
        measurement_data = "{}",
        diagnosis_data = "{}"
    )
    # Check if user ID is valid
    session.user_id = request.json.get("user_id")
    user = User.query.filter_by(id=session.user_id).first()
    if(user is None):
        return jsonify({"msg" : "Invalid user_id"})
    else:
        if(request.json.get("location") is None):
            return jsonify({"msg" : "location was not specified"})
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
        session = remove_instance_state(session)
        session['measurement_data'] = json.loads(session['measurement_data'])
        session['diagnosis_data'] = json.loads(session['diagnosis_data'])
        session['measurement_time'] = session_dict_get_kst(session, "measurement_time")
        session['diagnosis_time'] = session_dict_get_kst(session, "diagnosis_time")
        session['time'] = session_dict_get_kst(session, "time")
        return jsonify(session)

@sessions_routes.route('/<session_id>/measurements', strict_slashes=False)
def get_session_measurements(session_id):
    session = Session.query.filter_by(id=session_id).first()
    if(session is None):
        return {"msg" : "The session does not exist"}, 404
    else:
        measurement_data = json.loads(session.measurement_data)
        return jsonify(measurement_data)

@sessions_routes.route('/<session_id>/measurements', methods=["POST"], strict_slashes=False)
def create_session_measurements(session_id):
    session = Session.query.filter_by(id=session_id).first()
    if(session is None):
        return {"msg" : "The session does not exist"}, 404
    else:
        # request.get_json already returns a dict
        measurement_data = request.get_json()
        session.measurement_data = json.dumps(measurement_data)
        session.measurement_time = datetime.now()
        db.session.commit()
        return jsonify(measurement_data)

@sessions_routes.route('/<session_id>/diagnosis', strict_slashes=False)
def get_session_diagnosis(session_id):
    session = Session.query.filter_by(id=session_id).first()
    if(session is None):
        return {"msg" : "The session does not exist"}, 404
    else:
        diagnosis_data = json.loads(session.diagnosis)
        return jsonify(diagnosis_data)

@sessions_routes.route('/<session_id>/diagnosis', methods=["POST"], strict_slashes=False)
def create_session_diagnosis(session_id):
    session = Session.query.filter_by(id=session_id).first()
    if(session is None):
        return {"msg" : "The session does not exist"}, 404
    else:
        # request.get_json already returns a dict
        diagnosis_data = request.get_json()
        session.diagnosis_data = json.dumps(diagnosis_data)
        session.diagnosis_time = datetime.now()
        db.session.commit()
        return jsonify(diagnosis_data)