from flask import Blueprint
from server.schema import *
import random, datetime
import json
from server.app import db
from server.schema import *

clear_routes = Blueprint('clear_routes', __name__)

@clear_routes.route("/")
def clear_db():
    fill_data = []

    fill_data.append(User(username="patient1", password="password1", name="Patient1 Full Name"))
    fill_data.append(User(username="patient2", password="password2", name="Patient2 Full Name"))
    fill_data.append(User(username="patient3", password="password3", name="Patient3 Full Name"))
    fill_data.append(User(username="patient4", password="password4", name="Patient4 Full Name"))
    fill_data.append(User(username="patient5", password="password5", name="Patient5 Full Name"))
    fill_data.append(User(username="patient6", password="password6", name="Patient6 Full Name"))
    fill_data.append(User(username="patient7", password="password7", name="Patient7 Full Name"))

    fill_data.append(Car(username="medicar1", password="carpassword1", name="Medicar 1"))
    fill_data.append(Car(username="medicar2", password="carpassword2", name="Medicar 2"))

    fill_data.append(Car_Sensor(car_id=1, sensor_name="HGHT2000",
                        sensor_description="Laser-based height sensor",
                        measurement_key="height"))
    fill_data.append(Car_Sensor(car_id=1, sensor_name="MLX90614",
                        sensor_description="IR-based temperature sensor",
                        measurement_key="height"))
    fill_data.append(Car_Sensor(car_id=1, sensor_name="MAX30102",
                        sensor_description="Pulse Oximeter and Heart Rate sensor",
                        measurement_key="pulse_rate"))
    fill_data.append(Car_Sensor(car_id=1, sensor_name="MAX30102",
                        sensor_description="Pulse Oximeter and Heart Rate sensor",
                        measurement_key="blood_oxygen_saturation"))
    fill_data.append(Car_Sensor(car_id=1, sensor_name="Marsden WGT1002",
                        sensor_description="Next-gen electronic weight scale",
                        measurement_key="weight"))
    fill_data.append(Car_Sensor(car_id=1, sensor_name="PSI Blood V2",
                        sensor_description="Blood pressure sensor",
                        measurement_key="blood_pressure"))

    fill_data.append(Car_Sensor(car_id=2, sensor_name="HGHT2000",
                        sensor_description="A classic ruler",
                        measurement_key="height"))
    fill_data.append(Car_Sensor(car_id=2, sensor_name="MLX90614",
                        sensor_description="Contact-based temperature sensor",
                        measurement_key="height"))
    fill_data.append(Car_Sensor(car_id=2, sensor_name="MAX30102",
                        sensor_description="Pulse Oximeter and Heart Rate sensor",
                        measurement_key="pulse_rate"))
    fill_data.append(Car_Sensor(car_id=2, sensor_name="MAX30102",
                        sensor_description="Pulse Oximeter and Heart Rate sensor",
                        measurement_key="blood_oxygen_saturation"))
    fill_data.append(Car_Sensor(car_id=2, sensor_name="Toshiba Weighing scale",
                        sensor_description="Home weighing scale",
                        measurement_key="weight"))
    fill_data.append(Car_Sensor(car_id=2, sensor_name="PSI Blood V2",
                        sensor_description="Blood pressure sensor",
                        measurement_key="blood_pressure"))

    for i in range(0, 10):
        fill_data.append(generate_case())

    db.drop_all()
    db.create_all()
    db.session.bulk_save_objects(fill_data)
    db.session.commit()
    return { "msg" : "Dummy database reloaded" }

def generate_time():
    time = datetime.datetime.now() - datetime.timedelta(
        days=random.randint(0, 365*5),
        seconds=random.randint(0, 60),
        minutes=random.randint(0, 60),
        hours=random.randint(0, 24)
        )
    return time

def generate_case():
    measurement_data = {
        "height" : 160 + random.randint(-30, 15),
        "weight" : 60 + random.randint(-20, 30),
        "pulse_rate" : 75 + random.randint(-30, 30),
        "blood_pressure" : {
            "systolic" : 110 + random.randint(-20, 30),
            "diastolic" : 70 + random.randint(-20, 30)
        },
        "blood_oxygen_saturation" : 100 + random.randint(-5, 0)
    }
    
    diagnosis_data = {
        "diagnosis" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc lobortis euismod ligula blandit tempor. Nullam arcu ligula, sagittis vel nisl vitae, cursus sodales erat.",
        "additional_information": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    }

    case = Session(
        user_id = random.randint(1, 7),
        car_id = random.randint(1, 2),
        location = "Location" + str(random.randint(1, 5)),
        time = generate_time(),
        measurement_data = json.dumps(measurement_data, default=str),
        diagnosis_data = json.dumps(diagnosis_data, default=str)
    )
    case.measurement_time = case.time + datetime.timedelta(minutes=random.randint(5, 10), seconds=random.randint(0, 60))
    case.diagnosis_time = case.measurement_time + datetime.timedelta(minutes=random.randint(30, 60), seconds=random.randint(0, 60))
    return case
