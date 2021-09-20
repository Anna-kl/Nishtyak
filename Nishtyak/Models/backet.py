from Nishtyak import db
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class Backets(db.Model):
    __tablename__ = 'backets'

    id = db.Column(db.Integer, primary_key=True)
    dttmCreate = db.Column(DateTime(timezone=True), default=func.now())
    session = db.Column(db.Integer, nullable=True)
    id_user = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String())
    dttmClose = db.Column(DateTime(timezone=True))
    price=db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Backet: {self.name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    dttm_add = db.Column(DateTime(timezone=True), default=func.now())
    id_product=db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    id_backet=db.Column(db.Integer, db.ForeignKey('backets.id'), nullable=False)
    price=db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Orders: {self.name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}