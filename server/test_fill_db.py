from app import db, create_app
from schema import Case, Patient, Doctor
import random, datetime

def generate_case():
    case = Case(
        time = datetime.datetime.now() - datetime.timedelta(
            days=random.randint(0, 365*5),
            seconds=random.randint(0, 60),
            minutes=random.randint(0, 60),
            hours=random.randint(0, 24)
            ),
        patient_id = random.randint(1, 7),
        # doctor_id = random.randint(1, 7),
        doctor_id = None,
        pulse_rate = round(random.uniform(80.0, 120.0), 1),
        body_temperature = round(random.uniform(36.0, 41.0), 1),
        blood_oxygen_saturation = round(random.uniform(95.0, 99.0), 1),
        prescription = "",
        location = "Location" + str(random.randint(1, 5))
    )
    return case

fill_data = []

fill_data.append(Patient(username="patient1", password="password1", name="Patient1 Full Name"))
fill_data.append(Patient(username="patient2", password="password2", name="Patient2 Full Name"))
fill_data.append(Patient(username="patient3", password="password3", name="Patient3 Full Name"))
fill_data.append(Patient(username="patient4", password="password4", name="Patient4 Full Name"))
fill_data.append(Patient(username="patient5", password="password5", name="Patient5 Full Name"))
fill_data.append(Patient(username="patient6", password="password6", name="Patient6 Full Name"))
fill_data.append(Patient(username="patient7", password="password7", name="Patient7 Full Name"))

fill_data.append(Doctor(username="doctor1", password="dpassword1", name="Doctor1 Full Name", affiliation="institute1"))
fill_data.append(Doctor(username="doctor2", password="dpassword2", name="Doctor2 Full Name", affiliation="institute2"))
fill_data.append(Doctor(username="doctor3", password="dpassword3", name="Doctor3 Full Name", affiliation="institute3"))
fill_data.append(Doctor(username="doctor4", password="dpassword4", name="Doctor4 Full Name", affiliation="institute4"))
fill_data.append(Doctor(username="doctor5", password="dpassword5", name="Doctor5 Full Name", affiliation="institute5"))
fill_data.append(Doctor(username="doctor6", password="dpassword6", name="Doctor6 Full Name", affiliation="institute6"))
fill_data.append(Doctor(username="doctor7", password="dpassword7", name="Doctor7 Full Name", affiliation="institute7"))

for i in range(0, 25):
    fill_data.append(generate_case())

create_app().app_context().push()
db.drop_all()
db.create_all()
db.session.bulk_save_objects(fill_data)
db.session.commit()