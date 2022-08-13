from flask import Blueprint
from server.routes import * 

api_routes = Blueprint('api_routes', __name__)

api_routes.register_blueprint(auth_routes, url_prefix="/auth")
api_routes.register_blueprint(dump_routes, url_prefix="/dump")
api_routes.register_blueprint(users_routes, url_prefix="/users")
api_routes.register_blueprint(cars_routes, url_prefix="/cars")
api_routes.register_blueprint(sessions_routes, url_prefix="/sessions")
api_routes.register_blueprint(clear_routes, url_prefix="/clear")