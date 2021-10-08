from sqlalchemy import DateTime
from sqlalchemy.sql import func

from Nishtyak import db

class Bonus(db.Model):
    __tablename__='bonuses'

    id =  db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, nullable=False)
    idUser = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dttmUpdate =  db.Column(DateTime(timezone=True), default=func.now())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


db.create_all()