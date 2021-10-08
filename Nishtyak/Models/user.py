# Previous imports remain...
import datetime

import jwt
from sqlalchemy_utils.types.email import EmailType
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from Nishtyak import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(EmailType, unique=True, nullable=True)
    public_id = db.Column(db.String())
    phone = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    name = db.Column(db.String())
    dttm_add = db.Column(DateTime(timezone=True), default=func.now())
    coupon = db.Column(db.String(), nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self,  phone, public_id, password, coupon):
        self.phone = phone
        self.password = password
        self.public_id = public_id
        self.coupon = coupon

    def __repr__(self):
        return f"<User: {self.phone}>"

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                'Th1s1ss3cr3t',
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, 'Th1s1ss3cr3t')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class Code(db.Model):
    __tablename__ = 'codes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(12), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    createAt = db.Column(DateTime(timezone=True), default=func.now())

    def __init__(self, code, user_id):
        self.code = code
        self.user_id = user_id

    def __str__(self):
        return f"<Code: {self.code}>"

class Address(db.Model):
    __tablename__='address'
    id = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address = db.Column(db.String())
    floor = db.Column(db.Integer)
    house = db.Column(db.Integer)
    intercom = db.Column(db.String())
    apartment = db.Column(db.Integer)
    dttmUpdate = db.Column(DateTime(timezone=True), default=func.now())
    entrance = db.Column(db.Integer)

    def __init__(self, idUser, address, floor, house, intercom, apartment, dttmUpdate, entrance):
        self.idUser = idUser
        self.address = address
        self.floor = floor
        self.house = house
        self.intercom = intercom
        self.apartment = apartment
        self.dttmUpdate = dttmUpdate
        self.entrance = entrance

    def __str__(self):
        return f"<Address: {self.code}>"

    def check(self, address_new):
        if self.address != address_new.address:
            return False
        if self.apartment != address_new.apartment:
            return False
        if self.entrance != address_new.entrance:
            return False
        if self.floor != address_new.floor:
            return False
        if self.house != address_new.house:
            return False
        if self.intercom != address_new.intercom:
            return False
        return True

    def update(self, address):
        self.intercom = address.intercom
        self.address = address.address
        self.house = address.house
        self.entrance = address.entrance
        self.floor = address.floor
        self.apartment = address.apartment

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



db.create_all()
