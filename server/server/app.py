from flask import Flask
import secrets
from server.schema import *
from server.routes.auth_routes import jwt
from server.routes import api_routes
from flask_socketio import SocketIO

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['JWT_SECRET_KEY'] = secrets.token_hex()
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.secret_key = secrets.token_hex()
    db.init_app(app)
    jwt.init_app(app)
    return app

app = create_app()
app.register_blueprint(api_routes.api_routes, url_prefix="/API")
socketio = SocketIO(app)