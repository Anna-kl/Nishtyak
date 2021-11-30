# Previous imports remain...
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from Nishtyak import db


class Rules(db.Model):
    __tablename__ = 'rules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    productFor = db.Column(db.String())
    productOn = db.Column(db.String())
    price = db.Column(db.Integer)
    rule = db.Column(db.String())

    def __repr__(self):
        return f"<Rule: {self.name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


db.create_all()
