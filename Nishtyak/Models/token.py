from Nishtyak import db
from sqlalchemy import DateTime, func


class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    dttmCreate = db.Column(DateTime(timezone=True), default=func.now())
    accessToken = db.Column(db.String(), nullable=True)
    idUser = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    dttmExpired = db.Column(DateTime(timezone=True), default=func.now())
    status = db.Column(db.Boolean)

    def __str__(self):
        return f"<Token: {self.name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

db.create_all()
