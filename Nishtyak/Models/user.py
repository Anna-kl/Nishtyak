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

    def __repr__(self):
        return f"<Code: {self.code}>"


db.create_all()
