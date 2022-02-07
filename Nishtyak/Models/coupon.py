from Nishtyak import db
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class Coupon(db.Model):
    __tablename__ = 'coupons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    rule = db.Column(db.String())
    createAdd = db.Column(DateTime(timezone=True), default=func.now())
    closeAdd = db.Column(DateTime(timezone=True), default=func.now())
    idUser = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    option = db.Column(db.String())

    def __repr__(self):
        return f"<Coupon: {self.name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class UseCoupon(db.Model):
    __tablename__ = 'use_coupons'

    id = db.Column(db.Integer, primary_key=True)
    idCoupon = db.Column(db.Integer)
    idBacket = db.Column(db.Integer, db.ForeignKey('backets.id'), nullable=False)
    option = db.Column(db.String())

    def __repr__(self):
        return f"<Coupon: {self.name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


db.create_all()