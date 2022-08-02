from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_login import UserMixin

db = SQLAlchemy()

class Case(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime)
    patient_id = db.Column(db.Integer, ForeignKey("user.id"))
    doctor_id = db.Column(db.Integer, ForeignKey("user.id"))
    pulse_rate = db.Column(db.Float)
    body_temperature = db.Column(db.Float)
    blood_oxygen_saturation = db.Column(db.Float)
    prescription = db.Column(db.String(512))
    location = db.Column(db.String(256))


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(36))
    password = db.Column(db.String(128))
    user_type = db.Column(db.String(128))
    name = db.Column(db.String(256))
    __mapper_args__ = {"polymorphic_on" : user_type}

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

class Patient(User):
    __mapper_args__ = {"polymorphic_identity" : "patient"}

class Doctor(User):
    institution_id = db.Column(db.Integer, ForeignKey("institution.id"))
    __mapper_args__ = {"polymorphic_identity" : "doctor"}

class Institution(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256))