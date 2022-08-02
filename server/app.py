from threading import currentThread
from flask import Flask, redirect, url_for
from flask import request
from flask import render_template
from schema import db, Case, Patient, Doctor, User, Institution
from datetime import datetime
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import json
import secrets

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.secret_key = secrets.token_hex()
    db.init_app(app)
    return app

app = create_app()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.context_processor
def inject_header_data():
    if(isinstance(current_user, User)):
        return dict(
            doctor=Doctor.query.get(current_user.id),
            institution=Institution.query.get(Doctor.query.get(current_user.id).institution_id)
        )
    else:
        return dict()

@app.route("/API/diagnosis", methods=['POST', 'GET'])
def show_test_db():
    if(request.method == 'GET'):
        return render_template("test_db.html")
    elif(request.method == 'POST'):
        # Diagnosis data must include
        # patient username
        # patient name
        # doctor id
        # patient location
        # pulse rate
        # body temp
        # blood oxygen saturation


        # Create new patient if the patient does not exist
        # TODO: Figure out what to do with users whose password == None
        patient_list = db.session.query(Patient).filter(Patient.username == request.form["username"]).all()
        print("IN POST!!!")
        if(len(patient_list) == 0):
            new_patient = Patient(
                username = request.form["username"],
                password = None,
                name = request.form["name"],
            )

            db.session.add(new_patient)
            db.session.commit()
            patient_list.append(new_patient)

        new_case = Case(time=datetime.now(), prescription="",
            patient_id=patient_list[0].id,
            doctor_id=request.form["doctor_id"],
            pulse_rate=request.form["pulse_rate"],
            body_temperature=request.form["body_temperature"],
            blood_oxygen_saturation=request.form["blood_oxygen_saturation"],
            location=request.form["location"]
        )

        db.session.add(new_case)
        db.session.commit()
        return "success"

@app.route("/cases", methods=['GET'])
@login_required
def show_cases():
    cases = db.session.query(Case).filter(Case.doctor_id == current_user.id).all()
    for case in cases:
        case.patient_id = Patient.query.get(case.patient_id).username
        case.doctor_id = Doctor.query.get(case.doctor_id).username
    return render_template("cases.html", cases=cases)
    # return render_template("cases.html", doctor=Doctor.query.get(current_user.id),
                            # institution=Institution.query.get(Doctor.query.get(current_user.id).institution_id),
                            # cases=cases)

@app.route("/cases/<case_id>", methods=['GET'])
@login_required
def show_view_case(case_id):
    case = Case.query.get(case_id)
    patient = Patient.query.get(case.patient_id)
    doctor = Doctor.query.get(case.doctor_id)
    return render_template("diagnosis.html", case=case, patient=patient, doctor=doctor)

@app.route("/cases/<case_id>/prescription", methods=['POST'])
@login_required
def show_add_case_prescription(case_id):
    case = Case.query.get(case_id)
    prescription = request.form["prescription"]
    if(prescription == ""):
        case.doctor_id = None
    else:
        case.doctor_id = current_user.id
    case.prescription = prescription
    db.session.commit()
    return redirect(url_for('show_view_case', case_id=case_id))

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        user_list = db.session.query(User).filter(User.username == request.form["username"]).all()
        if(len(user_list) == 1 and user_list[0].password == request.form["password"]):
            loggedInUser = user_list[0]
            if(loggedInUser.user_type == "doctor"):
                login_user(Doctor.query.get(loggedInUser.id))
                return redirect(url_for("show_cases"))
            elif(loggedInUser.user_type == "patient"):
                login_user(Patient.query.get(loggedInUser.id))
                return redirect(url_for("logout")) # TODO: Implement APIs for user part...
        return redirect(url_for("login"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

def dump_jsonify(db_entry):
    entry = db_entry.__dict__
    return json.dumps(entry, default=str)

@app.route("/dump", methods=['GET'])
def show_dump():
    response=""

    response += "<br><b>user</b><br>"
    for user in User.query.all():
        response += dump_jsonify(user)
        response += "<br>"

    response += "<br><b>patients</b><br>"
    for patient in Patient.query.all():
        response += dump_jsonify(patient)
        response += "<br>"

    response += "<br><b>institutions</b><br>"
    for doctor in Institution.query.all():
        response += dump_jsonify(doctor)
        response += "<br>"

    response += "<br><b>doctors</b><br>"
    for doctor in Doctor.query.all():
        response += dump_jsonify(doctor)
        response += "<br>"

    response += "<br><b>cases</b><br>"
    for case in Case.query.all():
        response += dump_jsonify(case)
        response += "<br>"

    return response