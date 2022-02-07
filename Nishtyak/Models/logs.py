# Previous imports remain...
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from Nishtyak import db


class Logs(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    data = db.Column(db.String(), nullable=False)
    idUser = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dttm_add = db.Column(DateTime(timezone=True), default=func.now())
    type =  db.Column(db.Integer)

    def __repr__(self):
        return f"<Product: {self.name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

db.create_all()