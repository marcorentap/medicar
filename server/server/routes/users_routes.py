from flask import Blueprint, jsonify
from server.schema import User, Session
from server.utils.database_tools import list_convert_to_dict, convert_to_dict, sessions_pre_jsonify

users_routes = Blueprint('users_routes', __name__)

@users_routes.route("/", strict_slashes=False)
def get_users():
    users = User.query.all()
    users = list_convert_to_dict(users)
    return jsonify(users)

@users_routes.route('/<user_id>')
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if(user is None):
        return {"msg" : "The user does not exist"}, 404
    else:
        user = convert_to_dict(user)
        return jsonify(user)

@users_routes.route('/<user_id>/sessions', strict_slashes=False)
def get_user_sessions(user_id):
    user = User.query.filter_by(id=user_id).first()
    sessions = Session.query.filter_by(user_id=user.id)
    if(user is None):
        return {"msg" : "The user does not exist"}, 404
    else:
        sessions = sessions_pre_jsonify(sessions)
        return jsonify(sessions)