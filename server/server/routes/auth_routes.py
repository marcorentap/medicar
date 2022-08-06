from operator import methodcaller
from flask import request, Blueprint
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, get_jwt
from server.schema import User

jwt = JWTManager()
auth_routes = Blueprint('auth_routes', __name__)

blocklist = []
@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload['jti']
    return jti in blocklist

@auth_routes.route('/login', methods=['POST'], strict_slashes=False)
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    # Find user in database
    user = User.query.filter_by(username=username, password=password).first()
    # If user credentials are valid, authenticate
    if(user):
        access_token = create_access_token(identity=user.id)
        return {"access_token" : access_token}
    else:
        return {"msg" : "Bad username or password"}, 401

@auth_routes.route('/logout', methods=['POST'], strict_slashes=False)
@jwt_required()
def logout():
    blocklist.append(get_jwt()['jti'])
    return {"msg" : "Access token revoked"}