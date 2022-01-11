"""
The flask application package.
"""
import telebot
from sqlalchemy import func, desc
import uuid
from functools import wraps
import json
from flask_cors import CORS, cross_origin

from flask import Flask, jsonify, make_response, request

from datetime import datetime
from flask import render_template
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


from Nishtyak.Models.jeneral import SendPrice, CouponSend, SendOrder

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'akklimova@gmail.com'
app.config['MAIL_PASSWORD'] = 'Aa2537300'
app.config['MAIL_USE_SSL'] = True


api_key = '2047227856:AAG2mQL01K0avmGX1p2RzKPR9bbZHUQtfh4'

bot = telebot.TeleBot(api_key, parse_mode=None)

import Nishtyak.views
mail = Mail()
mail.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] \
    = "postgresql://dufuauvnmhhnbi:e04834417d5b33baf80de46ff78c145979019532d52e0019de70b1e83dbf36b6@ec2-34-254-69-72.eu-west-1.compute.amazonaws.com:5432/ddq1javfo02shs"
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:2537300@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']='Th1s1ss3cr3t'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from Nishtyak.Models.user import User, Code, Address, ShowUser
from Nishtyak.Models.menu import Product, Stock
from Nishtyak.Models.backet import Backets, Order, InfoOrder
from Nishtyak.Models.bonus import Bonus
from Nishtyak.Models.rules import Rules
from Nishtyak.Models.winner import Winner
from Nishtyak.Models.schedule import Schedule

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

      auth_header = request.headers.get('Authorization').split(' ')[1]

      try:
         user = User.decode_auth_token(auth_token=auth_header)
      except:
         return jsonify({'message': 'token is invalid'})

      return f(user, *args, **kwargs)
   return decorator

# This decorator takes the class/namedtuple to convert any JSON
# data in incoming request to.
def convert_input_to(class_=None):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            obj = class_(**request.get_json())
            return f(obj)
        return decorator_function
    return decorator

# Авторизация и регистрация
@app.route('/api/register/<phone>', methods=['GET'])
def signup_user(phone):
    hashed_password = generate_password_hash(phone, method='sha256')
    check = User.query.filter_by(phone=phone).first()
    if check:
        check_code = db.session.query(Code).filter_by(user_id=check.id).first()
        if check_code:
                db.session.query(Code).filter_by(user_id=check.id).delete()
                db.session.commit()

        code='1111'

        if True:
            new_code = Code(user_id=check.id, code=code)
            db.session.add(new_code)
            db.session.commit()
            return jsonify({'message': 'user found', 'code': 200})

    else:
        coupon = None
        new_user = User(public_id=str(uuid.uuid4()), phone=phone, password=hashed_password, coupon=coupon)
        db.session.add(new_user)
        db.session.commit()
        new_code = Code(user_id=new_user.id, code='1111')
        db.session.add(new_code)
        db.session.commit()
        bonus = Bonus(idUser=new_user.id, dttmUpdate = datetime.now(),
                      count=0)
        db.session.add(bonus)
        db.session.commit()
        return jsonify({'message': 'registered', 'code': 201})

@app.route('/api/register/check', methods=['POST'])
def check_code():
    auth = request.get_json()
    check = db.session.query(User).join(Code, User.id == Code.user_id).\
        filter(User.phone == auth['phone']).filter(Code.code == str(auth['code'])).first()
    if check:
        auth_token = check.encode_auth_token(check.id)
        return jsonify({'message': 'right code', 'code': 200,
                        'data': auth_token.decode('UTF-8')})
    else:
        return jsonify({'message': 'wrong code', 'code': 404})

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.get_json()

    user = User.query.filter_by(phone=auth['phone']).first()

    auth_token = user.encode_auth_token(user.id)
    return jsonify({'message': 'success', 'code': 200,
                    'token': auth_token.decode('UTF-8')})

# Работа с аккаунтом пользователя
@app.route('/api/user', methods=['GET'])
@token_required
def getAccount(current_user):
    user = db.session.query(User).filter_by(id=current_user).first()
    bonus = db.session.query(Bonus).filter(current_user == Bonus.idUser).first()
    user = ShowUser(user, bonus.count)
    return jsonify({'message': 'success', 'code': 200,
                    'data': user.as_dict()})

@app.route('/api/user', methods=['POST'])
@token_required
def UpdateAccount(current_user):
    json_data = request.get_json()
    db.session.query(User).filter_by(id=current_user)\
        .update(dict(json_data))
    db.session.commit()
    updateddata = User.query.filter_by(id=current_user).first()
    return jsonify({'message': 'success', 'code': 200,
                    'data': updateddata.as_dict()})

# Поиск адреса клиента
@app.route('/api/getAddress/<phone>', methods=['GET'])
def getAddress(phone):
    address = db.session.query(Address).join(User, User.id==Address.idUser).filter(User.phone == phone).first()
    if address is None:
        user = db.session.query(User).filter(User.phone == phone).first()
        if user is None:
           # coupon = generate_password_hash(phone[2:5], method='sha256')
            coupon = None
            hashed_password = generate_password_hash(phone, method='sha256')
            new_user = User(public_id=str(uuid.uuid4()), phone=phone, password=hashed_password, coupon=None)
            db.session.add(new_user)
            db.session.commit()
            bonus = Bonus(count = 0, idUser = new_user.id, dttmUpdate = datetime.now())
            db.session.add(bonus)
            db.session.commit()
            return jsonify({'message': 'success', 'code': 404,
                    'data': new_user.id})
        else:
            return jsonify({'message': 'success', 'code': 404,
                            'data': user.id})
    else:
        return jsonify({'message': 'success', 'code': 200,
                        'data': address.as_dict()})

# Поиск адреса в базе
@app.route('/api/searchAddress', methods=['POST'])
def searchAddress():
    address=request.get_json()
    search = request.get('https://geocode-maps.yandex.ru/1.x/?apikey=a2c8035f-05f9-4489-aea1-ad9b2a841572&geocode={0}&format=json'
                         .format(address))
    return jsonify({'message': 'success', 'code': 404,
                    'data': address})

# создание заказа
@app.route('/api/createOrder/', methods=['POST'])
@convert_input_to(SendOrder)
def createOrder(order):
    try:
        address = db.session.query(Address).filter(Address.idUser == order.idUser).first()
        if address is None:
            if order.selfPickup == False:
                address = Address(idUser=order.idUser, address=order.address, floor=order.floor,
                                  house=order.house, intercom=order.intercom, apartment=order.apartment,
                                  dttmUpdate=datetime.now(), entrance=order.entrance)
                db.session.add(address)
                db.session.commit()
        elif address.check(order) == False:
            address.update(order)
        if order.selfPickup == True:
            infoOrder = InfoOrder(idAddress=-1, dttmCreate=datetime.now(),
                                  idBacket=order.idBacket, comment=order.comment, appliances=order.appliances,
                                  pay=None, status='create', sale=order.sale)
        else:
            infoOrder = InfoOrder(idAddress=address.id, dttmCreate=datetime.now(),
                                  idBacket=order.idBacket, comment=order.comment, appliances=order.appliances,
                                  pay=order.pay, status='create', sale=order.sale)
        backet = db.session.query(Backets).filter(Backets.id == order.idBacket).first()
        backet.status = 'accepted'
        backet.idUser = order.idUser

        db.session.add(infoOrder)
        db.session.commit()
        backet.price = order.totalPrice
        bonus = db.session.query(Bonus).filter(Bonus.idUser == order.idUser).first()
        if bonus is None:
            bonus = Bonus(count = order.totalPrice*0.05, idUser = order.idUser,
                            dttmUpdate =  datetime.now())
            db.session.add(bonus)
        else:
            if order.sale == 'bonus':
                bonus.count = 0
            bonus.count += order.totalPrice*0.05
            bonus.dttmUpdate = datetime.now()
        if order.sale == 'coupon':
            user = db.session.query(User).filter(User.id == order.idUser).first()
            user.coupon = None
        db.session.commit()
        send=dict(
            bonus = bonus.count,
            idOrder = infoOrder.id,
            totalPrice = order.totalPrice
        )
        products = db.session.query(Order, Product).join(Product, Order.idProduct == Product.id)\
            .filter(Order.idBacket == order.idBacket).all()
        user = db.session.query(User).filter(User.id == order.idUser).first()
        backet.idUser = user.id
        backet.dttmClose = datetime.now()
        db.session.commit()
        msg = Message('Новый заказ',
                      sender='akklimova@gmail.com',
                      recipients=['klimova_88@mail.ru'])
        msg.body = "Клиент - {0}\n".format(user.phone)
        if order.selfPickup == False:
            msg.body += "Адрес доставки - {0}, дом {1}, квартира - {2}," \
                   "подъезд - {3}, этаж - {4}, код домофона - {5}\n" \
                   "Оплата - {6}\n" \
                   "Комментарий - {7}\n" \
                   "Приборов - {8}\n" \
                   "Заказ:\n".format(address.address, address.house,
                                     address.apartment, address.entrance, address.floor,
                                     address.intercom, order.pay, order.comment, order.appliances,
                                     )
        else:
            msg.body += 'Самовывоз\n'
        for p in products:
            msg.body+='{0}, количество - {1}'.format(p.Product.name, p.Order.count)
            if p.Order.toping is not None:
                msg.body += ' {0}'.format(p.Order.toping)
            msg.body += '\n'
        msg.body+='Сумма - {0}\n' \
                  'Скидка - {1}\n'.format(order.totalPrice, order.sale)
        msg.body += 'Комментарий - {0}\n' \
                    'Приборов - {1}'.format(order.comment, order.appliances)

        #mail.send(msg)
        bot.send_message(604587575, msg.body)
        bot.send_message(1145917265, msg.body)
        return jsonify({'message': 'success', 'code': 201,
                        'data': send })
    except Exception as e:
        bot.send_message(604587575, 'Ошибка при заказе, User - {0}'.format(order.idUser))
        bot.send_message(1145917265, 'Ошибка при заказе, User - {0}'.format(order.idUser))
        return jsonify({'message': 'error', 'code': 400,
                        'data': ''})


# меню и акции
@app.route('/api/product', methods=['GET'])
def get_product():
    products = list(map(lambda x: x.as_dict(), db.session.query(Product).all()))
    return jsonify({'message': '', 'code': 200, 'data': products})

@app.route('/api/stock', methods=['GET'])
def get_stock():
    products = list(map(lambda x: x.as_dict(), Stock.query.all()))
    return jsonify({'message': '', 'code': 200, 'data': products})

#удалить продукт
@app.route('/api/deleteOrder', methods=['POST'])
@convert_input_to(Order)
def delete_order(sendOrder):
    order = db.session.query(Order).filter(Order.idBacket == sendOrder.idBacket)\
        .filter(Order.idProduct == sendOrder.idProduct)
    if order.first().toping == 'gift':
        backet = db.session.query(Backets).filter(Backets.id == sendOrder.idBacket).first()
        if backet.option == 'gift':
            backet.option = None
    order.delete()
    db.session.commit()
    return jsonify({'message': '', 'code': 200, 'data': ''})

# работа с корзиной
@app.route('/api/backet', methods=['POST'])
@convert_input_to(Backets)
def createBacket(backet):
    backetOld = db.session.query(Backets).filter(Backets.session == backet.session).first()
    if backetOld is None:
        db.session.add(backet)
        db.session.commit()
        return jsonify({'message': '', 'code': 200, 'data': backet.id})
    else:
        backetOld.update(backet)
        db.session.commit()
        return jsonify({'message': '', 'code': 200, 'data': backetOld.id})

@app.route('/api/getCount/<session>', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content- Type'])
def getCount(session):

    try:
        backet = db.session.query(Order).join(Backets, Backets.id == Order.idBacket)\
        .filter(Backets.session==session).all()
        return jsonify({'message': '', 'code': 200, 'data': backet.__len__()})
    except Exception as ex:
        return jsonify({'message': '', 'code': 400, 'data': ''})

@app.route('/api/getIdBacket/<session>', methods=['GET'])
def getIdBacket(session):
    backet = db.session.query(Backets).filter(Backets.session==session).first()
    if backet is not None:
        return jsonify({'message': '', 'code': 200, 'data': backet.id})
    else:
        return jsonify({'message': '', 'code': 404, 'data': ''})


@app.route('/api/order', methods=['POST'])
@convert_input_to(Order)
def addProduct(order):
    orders = db.session.query(Order).filter(Order.idBacket == order.idBacket)\
        .filter(Order.idProduct == order.idProduct).first()
    if orders is not None:
        orders.count += order.count
    else:
        db.session.add(order)
    db.session.commit()
    return jsonify({'message': '', 'code': 200, 'data': order.id})


@app.route('/api/addgift', methods=['POST'])
@convert_input_to(Order)
def addGift(order):
    backet = db.session.query(Backets).filter(Backets.id == order.idBacket).first()
    if order.idProduct != -1:
        order.toping = 'gift'

        backet.option = 'gift'
        db.session.add(order)
    else:
        backet.option = 'None'
        order.toping = 'None'

    db.session.commit()
    return jsonify({'message': '', 'code': 201, 'data': order.id})

@app.route('/api/getListProducts/<session>', methods=['GET'])
def getListProducts(session):
    backet = db.session.query(Backets).filter(Backets.session==session and (Backets.status == 'active')).first()
    res = []
    flagGift = False
    if backet is not None:
        results = db.session.query(Order, Product).join(Product, Product.id == Order.idProduct).filter(Order.idBacket==backet.id).all()
        price = db.session.query(func.sum(Order.price * Order.count)).filter(Order.idBacket==backet.id).first()
        rule = db.session.query(Rules).filter(Rules.option == 'gift').all()
        for order, product in results:
            flagAdd = True
            if order.toping == 'None':
                continue
            if order.toping == 'gift':
                flagGift = True
                for r in rule:

                    if order.idProduct in json.loads(r.productOn):
                        if price[0] < r.condition:
                            db.session.query(Order).filter(Order.id == order.id).delete()
                            backet.option = None
                            db.session.commit()
                            return jsonify({'message': '', 'code': 400, 'data': ''})

            if flagAdd:
                res.append({
                    'id': order.id,
                    'dttmAdd': order.dttmAdd,
                    'idBacket': order.idBacket,
                    'count': order.count,
                    'idProduct': order.idProduct,
                    'structure': product.structure,
                    'price': order.price,
                    'name': product.name,
                    'weight': product.weight
                })
        flagAdd = False
        if flagGift == False and backet.option == 'gift':
            backet.option = None
            db.session.commit()
        if backet.option is None and price[0] is not None:
            for r in rule:
                if int(r.condition) <= price[0]:
                     flagAdd = True
        if backet.option == 'None':
            backet.option = None
            db.session.commit()
        code = 200
        if flagAdd:
            code = 201
        return jsonify({'message': '', 'code': code,
                        'data':res})
    else:
        return jsonify({'message': '', 'code': 404, 'data': ''})


# получить подарки
@app.route('/api/LastRaffle', methods=['GET'])
def getLastRaffle():
    subquery = db.session.query(Winner).order_by(desc(Winner.createAt)).first()
    raffle = db.session.query(Winner).filter(func.DATE(Winner.createAt) == func.DATE(subquery.createAt)).order_by(Winner.place).all()
    send = list(map(lambda x: x.as_dict(), raffle))
    return jsonify({'message': '', 'code': 200, 'data': send})

# расчет стоимости
@app.route('/api/getTotalPrice', methods=['POST'])
@convert_input_to(SendPrice)
def getTotalPrice(price):
    products = db.session.query(Product, Order).join(Order) \
        .filter(Order.idBacket == price.idBacket).all()
    sendPrice = 0
    for i in products:
        sendPrice += i.Order.price * i.Order.count
    if price.selfPicker:
        sendPrice = sendPrice*0.9
    # user = db.session.query(User).filter(User.id == price.idUser).first()
    # if user is None:
    #     coupon = CouponSend(None, None, sendPrice)
    #     return jsonify({'message': '', 'code': 400, 'data': sendPrice})
    if price.idUser is None or price.idUser == -1:
        coupon = CouponSend(None,None, sendPrice)
        return jsonify({'message': '', 'code': 200, 'data': coupon.serialize()})
    else:
        user = db.session.query(User).filter(User.id == price.idUser).first()
        if user.coupon is not None:
            sendPrice = round(sendPrice*0.8)
          #  bonus = db.session.query(Bonus).filter(Bonus.idUser == user.id).first()
            coupon = CouponSend(user.coupon, 0, sendPrice)
            return jsonify({'message': '', 'code': 201, 'data': coupon.serialize()})
        else:
            bonuses = db.session.query(Bonus).filter(Bonus.idUser == user.id).first()
            if price.isBonuses:
                sendPrice = sendPrice - bonuses.count
                coupon = CouponSend(user.coupon, bonuses.count, sendPrice)
                return jsonify({'message': '', 'code': 201, 'data': coupon.serialize()})
            else:
                coupon = CouponSend(user.coupon, bonuses.count, sendPrice)
                return jsonify({'message': '', 'code': 201, 'data': coupon.serialize()})

@app.route('/api/getOptionalProduct/<id>', methods=['GET'])
def getOptionalProduct(id):
    rules = db.session.query(Rules).all()
    for rule in rules:
        idPruductFor = json.loads(rule.productFor)
        if int(id) in idPruductFor:
            idProductsOn = db.session.query(Product)\
                .filter(Product.id.in_(json.loads(rule.productOn))).all()
            products = list(map(lambda x: x.as_dict(), idProductsOn))
            rulesSend = rule.as_dict()
            return jsonify({'message': '', 'code': 200, 'data': products, 'rule': rulesSend})
    return jsonify({'message': '', 'code': 400, 'data': ''})

@app.route('/api/checkProduct/<id>', methods=['GET'])
def checkProduct(id):
    rules = db.session.query(Rules).all()
    for rule in rules:
        idPruductFor = json.loads(rule.productFor)
        if int(id) in idPruductFor:
            return jsonify({'message': '', 'code': 200, 'data': ''})
    return jsonify({'message': '', 'code': 400, 'data': ''})

@app.route('/api/getGift/<session>', methods=['GET'])
def getGift(session):
    rules = db.session.query(Rules).filter(Rules.option == 'gift').all()
    backet = db.session.query(Backets).filter(Backets.session == session and (Backets.status == 'active')).first()
    if backet.option == 'gift':
        return jsonify({'message': '', 'code': 400, 'data': ''})
    price = db.session.query(func.sum(Order.price * Order.count)).filter(Order.idBacket == backet.id).first()
    product = []
    for rule in rules:
        if int(rule.condition) <= price[0]:
            pr = db.session.query(Product) \
                .filter(Product.id.in_(json.loads(rule.productOn))) \
                .filter(Product.status == True).all()
            for i in pr:
                i.price = rule.price
            product.extend(pr)
    products = list(map(lambda x: x.as_dict(), product))
    rulesSend = {
        'rule': 'onetoone',
         'title': 'Подарок'
    }
    return jsonify({'message': '', 'code': 200, 'data': products, 'rule': rulesSend})

# region schedule

@app.route('/api/getSchedule', methods=['GET'])
def getSchedule():
    d = datetime.now()
    schedule = db.session.query(Schedule).filter(
        Schedule.dateOpen <= datetime.now()).filter(Schedule.dateClose >= datetime.now())\
        .filter(Schedule.status).filter(Schedule.rule == 'one').first()
    if schedule:
        return jsonify({'message': '', 'code': 200, 'data': schedule.as_dict()})
    else:
        schedule = db.session.query(Schedule).filter(Schedule.status).filter(Schedule.rule == 'regular').first()
        if schedule:
            return jsonify({'message': '', 'code': 200, 'data': schedule.as_dict()})
        return jsonify({'message': '', 'code': 404})


# end region schedule

#region getHistory
@app.route('/api/getHistoryBacket', methods=['GET'])
@token_required
def getHistoryOrder(current_user):
    user = db.session.query(User).filter(User.id == current_user).first()
    orders = db.session.query(Backets).filter(Backets.idUser == user.id).\
        filter(Backets.status == 'accepted').all()
    for i in orders:
        order = db.session.query(Order).filter(Order.idBacket == i.id).all()
        desc = []
        for temp_order in order:
            product = db.session.query(Product).filter(Product.id == temp_order.idProduct).first()
            desc.append(product.name)
        i.desc = ','.join(desc)
    orders = list(map(lambda x: x.sendBacketInfo(), orders))
    return jsonify({'message': '', 'code': 200, 'data': orders})