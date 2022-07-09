import requests

SERVER = "https://medicar.marcorentap.com"

def add_diagnosis(username, name, location, pulse_rate, body_temp, blood_pressure):
    r = requests.post(SERVER, data={
        'username' : username,
        'name' : name,
        'location' : location,
        'pulse_rate' : pulse_rate,
        'body_temp' : body_temp,
        'blood_pressure' : blood_pressure,
    })