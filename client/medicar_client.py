import requests

SERVER = "https://medicar.marcorentap.com"
# SERVER = "http://127.0.0.1:5000"

def add_diagnosis(username: str, name: str, location: str, pulse_rate: float, body_temperature: float, blood_oxygen_saturation: float):
    r = requests.post(SERVER + "/API/diagnosis", data={
        'username' : username,
        'name' : name,
        'location' : location,
        'pulse_rate' : pulse_rate,
        'body_temperature' : body_temperature,
        'blood_oxygen_saturation' : blood_oxygen_saturation,
    })