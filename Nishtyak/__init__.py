"""
The flask application package.
"""

import uuid
from functools import wraps

from flask_cors import CORS

from flask import Flask, jsonify, make_response, request

from datetime import datetime
from flask import render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
import Nishtyak.views

app.config['SQLALCHEMY_DATABASE_URI'] \
    = "postgresql://dufuauvnmhhnbi:e04834417d5b33baf80de46ff78c145979019532d52e0019de70b1e83dbf36b6@ec2-34-254-69-72.eu-west-1.compute.amazonaws.com:5432/ddq1javfo02shs"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']='Th1s1ss3cr3t'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from Nishtyak.Models.user import User, Code
from Nishtyak.Models.menu import Product

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


# Авторизация и регистрация
@app.route('/api/register/<phone>', methods=['GET'])
def signup_user(phone):
    phone = phone[1:len(phone)].replace('(', '').replace(')', '')
    hashed_password = generate_password_hash(phone, method='sha256')
    check = User.query.filter_by(phone=phone).first()
    if check:
        check_code = db.session.query(Code).filter_by(user_id=check.id).first()
        if check_code:
                db.session.query(Code).filter_by(user_id=check.id).delete()
                db.session.commit()

        code='1111'
        # code = str(random.randint(1000, 9999))
        #
        # request = requests.get('https://api.ucaller.ru/v1.0/initCall?service_id=424899&key=87P72MxNzTKK2IaHC4J2dtCvckI8dr3C&phone={0}&code={1}'.
        #                        format(phone, code))
        # result = json.loads(request.content.decode())

        # if (result['status']):
        if True:
            new_code = Code(user_id=check.id, code=code)
            db.session.add(new_code)
            db.session.commit()
            return jsonify({'message': 'user found', 'code': 200})
        else:
            return jsonify({'message': 'not found', 'code': 404})
    else:
        coupon = generate_password_hash(phone[2:5], method='sha256')
        new_user = User(public_id=str(uuid.uuid4()), phone=phone, password=hashed_password, coupon=coupon[1:9])
        db.session.add(new_user)
        db.session.commit()
        new_code = Code(user_id=new_user.id, code='1111')
        db.session.add(new_code)
        db.session.commit()
        return jsonify({'message': 'registered', 'code': 201})

@app.route('/api/register/check', methods=['POST'])
def check_code():
    auth = request.get_json()
    auth['phone'] = auth['phone'].replace('+', '').replace('(', '').replace(')', '')
    check = User.query.join(Code, User.id == Code.user_id).\
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
    user = User.query.filter_by(id=current_user).first()
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

@app.route('/api/product', methods=['GET'])
def home():
    products = list(map(lambda x: x.as_dict(), Product.query.all()))
    return jsonify({'message': '', 'code': 200, 'data': products})


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
