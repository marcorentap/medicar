from flask import Blueprint, jsonify, json
from server.schema import Car, Car_Sensor
from server.utils.database_tools import convert_to_dict
from server.utils.database_tools import list_convert_to_dict

cars_routes = Blueprint('cars_routes', __name__)

def add_car_sensors(car_dict):
    sensors = Car_Sensor.query.filter_by(car_id=car_dict["id"])
    sensors = list_convert_to_dict(sensors)
    sensors = [json.dumps(sensor) for sensor in sensors]
    car_dict["sensors"] = [json.loads(sensor) for sensor in sensors]
    return car_dict

@cars_routes.route("/", strict_slashes=False)
def get_cars():
    cars = Car.query.all()
    cars = list_convert_to_dict(cars)
    return jsonify(cars)

@cars_routes.route('/<car_id>')
def get_car(car_id):
    car = Car.query.filter_by(id=car_id).first()
    if(car is None):
        return {"msg" : "The car does not exist"}, 404
    else:
        car = convert_to_dict(car)
        car = add_car_sensors(car)
        return jsonify(car)

@cars_routes.route('/<car_id>/sensors', strict_slashes=False)
def get_car_sensors(car_id):
    car = Car.query.filter_by(id=car_id).first()
    if(car is None):
        return {"msg" : "The car does not exist"}, 404
    else:
        sensors = Car_Sensor.query.filter_by(car_id=car_id)
        sensors = list_convert_to_dict(sensors)
        sensors = [json.dumps(sensor) for sensor in sensors]
        sensor_list = [json.loads(sensor) for sensor in sensors]
        return jsonify(sensor_list)