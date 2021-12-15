import datetime

import jwt
from sqlalchemy_utils.types.email import EmailType
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from Nishtyak import db

class Winner(db.Model):
    __tablename__ = 'winners'

    id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    createAt = db.Column(DateTime(timezone=True), default=func.now())
    status = db.Column(db.Boolean)
    phone = db.Column(db.String())

    def __init__(self, place, user_id, createAt, status, phone):
        self.place = place
        self.user_id = user_id
        self.createAt = createAt
        self.status = status
        self.phone = phone

    def __str__(self):
        return f"<Winner: {self.code}>"


db.create_all()