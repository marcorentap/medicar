import requests

SERVER = "https://medicar.marcorentap.com"

def add_diagnosis(username: str, name: str, location: str, pulse_rate: int, body_temp: float, blood_pressure: int):
    r = requests.post(SERVER, data={
        'username' : username,
        'name' : name,
        'location' : location,
        'pulse_rate' : pulse_rate,
        'body_temp' : body_temp,
        'blood_pressure' : blood_pressure,
    })