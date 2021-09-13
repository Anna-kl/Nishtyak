# Previous imports remain...
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from Nishtyak import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),  nullable=False)
    structure = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    dttm_add = db.Column(DateTime(timezone=True), default=func.now())
    sale = db.Column(db.Integer, nullable=True)
    icon = db.Column(db.String(), nullable=False)
    tag = db.Column(db.String(), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    kilocalories = db.Column(db.Integer)

    def __repr__(self):
        return f"<Product: {self.name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

db.create_all()