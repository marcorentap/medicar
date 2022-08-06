from flask import Blueprint, jsonify
from server.schema import User
from server.utils.database_tools import list_remove_instance_state, remove_instance_state

users_routes = Blueprint('users_routes', __name__)

@users_routes.route("/", strict_slashes=False)
def get_users():
    users = User.query.all()
    users = list_remove_instance_state(users)
    return jsonify(users)

@users_routes.route('/<user_id>')
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if(user is None):
        return {"msg" : "The user does not exist"}, 404
    else:
        user = remove_instance_state(user)
        return jsonify(user)