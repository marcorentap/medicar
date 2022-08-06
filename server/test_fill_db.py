from server.app import db, create_app
from server.schema import *
import random, datetime
import json

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

    case = Session(
        user_id = random.randint(1, 7),
        car_id = random.randint(1, 7),
        location = "Location" + str(random.randint(1, 5)),
        measurement_time = datetime.datetime.now() - datetime.timedelta(
            days=random.randint(0, 365*5),
            seconds=random.randint(0, 60),
            minutes=random.randint(0, 60),
            hours=random.randint(0, 24)
            ),
        measurement_data = json.dumps(measurement_data, default=str),
        diagnosis_data = ""
    )
    print(json.dumps(case.__dict__, default=str))
    return case

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
fill_data.append(Car(username="medicar3", password="carpassword3", name="Medicar 3"))
fill_data.append(Car(username="medicar4", password="carpassword4", name="Medicar 4"))
fill_data.append(Car(username="medicar5", password="carpassword5", name="Medicar 5"))
fill_data.append(Car(username="medicar6", password="carpassword6", name="Medicar 6"))


for i in range(0, 1):
    fill_data.append(generate_case())

create_app().app_context().push()
db.drop_all()
db.create_all()
db.session.bulk_save_objects(fill_data)
db.session.commit()