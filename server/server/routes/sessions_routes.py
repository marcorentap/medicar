from datetime import datetime
from flask import Blueprint, jsonify, request
from server.schema import Session, db, User, Car
from server.utils.database_tools import sessions_pre_jsonify, session_pre_jsonify
from server.routes.cars_routes import get_car
import json

sessions_routes = Blueprint('sessions_routes', __name__)


@sessions_routes.route("/", strict_slashes=False)
def get_sessions():
    sessions = Session.query.all()
    sessions = sessions_pre_jsonify(sessions)
    return jsonify(sessions)

@sessions_routes.route("/", methods=["POST"], strict_slashes=False)
def create_session():
    session = Session(
        car_id = None,
        time = datetime.now(),
        measurement_data = "{}",
        diagnosis_data = "{}"
    )
    if(request.json.get("location") is None or request.json.get("user_id") is None):
        return {"msg" : "Invalid arguments. Expected location and user_id"}, 400

    # Check if user ID is valid
    session.user_id = request.json.get("user_id")
    user = User.query.filter_by(id=session.user_id).first()
    if(user is None):
        return {"msg" : "The user_id does not exist"}, 404
    else:
        session.location = request.json.get("location")
        db.session.add(session)
        db.session.commit()
        return get_session(session_id=session.id)

@sessions_routes.route('/<session_id>')
def get_session(session_id):
    session = Session.query.filter_by(id=session_id).first()
    if(session is None):
        return {"msg" : "The session_id does not exist"}, 404
    else:
        session = session_pre_jsonify(session)
        return jsonify(session)

@sessions_routes.route('/<session_id>/measurements', strict_slashes=False)
def get_session_measurements(session_id):
    session = Session.query.filter_by(id=session_id).first()
    if(session is None):
        return {"msg" : "The session_id does not exist"}, 404
    else:
        measurement_data = json.loads(session.measurement_data)
        return jsonify(measurement_data)

@sessions_routes.route('/<session_id>/measurements', methods=["POST"], strict_slashes=False)
def create_session_measurements(session_id):
    session = Session.query.filter_by(id=session_id).first()
    if(session is None):
        return {"msg" : "The session_id does not exist"}, 404
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
        return {"msg" : "The session_id does not exist"}, 404
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

@sessions_routes.route('/<session_id>/attach-car', methods=["POST"], strict_slashes=False)
def attach_car(session_id):
    if(request.json.get("car_id") is None):
        return {"msg" : "Invalid arguments. Expected car_id"}, 400

    session = Session.query.filter_by(id=session_id).first()
    if(session is None):
        return {"msg" : "The session does not exist"}, 404

    car_id = request.json.get("car_id")
    car = Car.query.filter_by(id=car_id).first()
    if(car is None):
        return {"msg" : "The car_id does not exist"}, 404

    session.car_id = car_id
    db.session.commit()

    return(get_session(session_id=session.id))

@sessions_routes.route('/<session_id>/car')
def session_get_car(session_id):
    session = Session.query.filter_by(id=session_id).first()
    if(session is None):
        return {"msg" : "The session does not exist"}, 404
    if(session.car_id is None):
        return {}
    else:
        return get_car(session.car_id)