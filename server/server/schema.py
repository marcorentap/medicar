from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class Session(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    car_id = db.Column(db.Integer, ForeignKey("user.id"))
    location = db.Column(db.String(256))
    time = db.Column(db.DateTime)
    measurement_time = db.Column(db.DateTime)
    diagnosis_time = db.Column(db.DateTime)
    measurement_data = db.Column(db.String(8192))
    diagnosis_data = db.Column(db.String(4096))

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(36))
    password = db.Column(db.String(128))
    name = db.Column(db.String(256))

class Car(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(36))
    password = db.Column(db.String(128))
    name = db.Column(db.String(256))

# Stores the sensors available on the cars
class Car_Sensor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    car_id = db.Column(db.Integer, ForeignKey("car.id"))
    sensor_name = db.Column(db.String(256))
    sensor_description = db.Column(db.String(4096))
    measurement_key = db.Column(db.String(256))