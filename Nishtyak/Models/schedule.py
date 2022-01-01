from Nishtyak import db
from sqlalchemy import DateTime
from sqlalchemy.sql import func

class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    createAt = db.Column(DateTime(timezone=False), default=func.now())
    dateOpen = db.Column(DateTime(timezone=False), default=func.now())
    dateClose = db.Column(DateTime(timezone=False), default=func.now())
    reason = db.Column(db.String())
    status = db.Column(db.Boolean)
    rule = db.Column(db.String())
    icon = db.Column(db.String())

    def __str__(self):
        return f"Режим работы: {self.name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


db.create_all()
