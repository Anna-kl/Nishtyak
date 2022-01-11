
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from Nishtyak import db

class Backets(db.Model):
    __tablename__ = 'backets'

    id = db.Column(db.Integer, primary_key=True)
    dttmCreate = db.Column(DateTime(timezone=True), default=func.now())
    session = db.Column(db.String(), nullable=True)
    idUser = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String())
    option = db.Column(db.String())
    dttmClose = db.Column(DateTime(timezone=True))
    price=db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f"<Backet: {self.name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, backet):
        self.status = backet.status
        if backet.status == 'close':
            self.dttmClose = backet.dttmCreate
        else:
            self.dttmCreate = backet.dttmCreate

    def sendBacketInfo(self):
        return {
            'dttmClose': self.dttmClose,
            'price': self.price,
            'desc': self.desc
        }



class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    dttmAdd = db.Column(DateTime(timezone=True), default=func.now())
    idProduct=db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    idBacket=db.Column(db.Integer, db.ForeignKey('backets.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float)
    toping = db.Column(db.String())

    def __str__(self):
        return f"<Orders: {self.name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class InfoOrder(db.Model):
    __tablename__='infoOrders'

    id = db.Column(db.Integer, primary_key=True)
    idAddress = db.Column(db.Integer,  nullable=False)
    dttmCreate = db.Column(DateTime(timezone=True), default=func.now())
    idBacket = db.Column(db.Integer, db.ForeignKey('backets.id'), nullable=False)
    comment = db.Column(db.String())
    appliances = db.Column(db.Integer)
    pay = db.Column(db.String())
    status = db.Column(db.String())
    selfPickup = db.Column(db.Boolean, default=False, nullable=False)
    sale = db.Column(db.String())

db.create_all()