from flask import Blueprint, jsonify
from server.schema import Car
from server.utils.database_tools import list_remove_instance_state, remove_instance_state

cars_routes = Blueprint('cars_routes', __name__)

@cars_routes.route("/", strict_slashes=False)
def get_cars():
    cars = Car.query.all()
    cars = list_remove_instance_state(cars)
    return jsonify(cars)

@cars_routes.route('/<car_id>')
def get_car(car_id):
    car = Car.query.filter_by(id=car_id).first()
    if(car is None):
        return {"msg" : "The car does not exist"}, 404
    else:
        car = remove_instance_state(car)
        return jsonify(car)
