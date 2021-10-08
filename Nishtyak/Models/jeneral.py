class SendPrice:
    idBacket = 0
    idUser = 0
    isBonuses=False

    def __init__(self, idBacket, idUser, isBonuses):
        self.idBacket = idBacket
        self.idUser = idUser
        self.isBonuses = isBonuses


class CouponSend:
    coupon = ''
    bonuses = 0
    totalPrice = 0

    def __init__(self, coupon, bonuses, totalPrice):
        self.coupon = coupon
        self.bonuses = bonuses
        self.totalPrice = totalPrice

    def serialize(self):
        return {
            'coupon': self.coupon,
            'bonuses': self.bonuses,
            'totalPrice': self.totalPrice,
        }


class SendOrder:

    def __init__(self, address, house, floor, idUser, intercom,
                 apartment, entrance, comment, pay, idBacket, totalPrice,
                 selfPickup, appliances, sale ):
        self.address = address
        self.house = house
        self.floor= floor
        self.idUser = idUser
        self.intercom = intercom
        self.apartment = apartment
        self.entrance = entrance
        self.comment = comment
        self.pay = pay
        self.appliances = appliances
        self.idBacket = idBacket
        self.totalPrice = totalPrice
        self.selfPickup = selfPickup
        self.sale = sale