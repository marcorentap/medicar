from flask import Blueprint
from server.schema import *
import json

dump_routes = Blueprint('dump_routes', __name__)

def dump_jsonify(db_entry):
    entry = db_entry.__dict__
    return json.dumps(entry, default=str)

@dump_routes.route("/")
def dump():
    response=""

    response += "<br><b>user</b><br>"
    for user in User.query.all():
        response += dump_jsonify(user)
        response += "<br>"

    response += "<br><b>patients</b><br>"
    for patient in Patient.query.all():
        response += dump_jsonify(patient)
        response += "<br>"

    response += "<br><b>cars</b><br>"
    for doctor in Car.query.all():
        response += dump_jsonify(doctor)
        response += "<br>"

    response += "<br><b>cases</b><br>"
    for case in Session.query.all():
        response += dump_jsonify(case)
        response += "<br>"

    return response
