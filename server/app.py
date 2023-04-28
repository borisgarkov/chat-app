from flask import Flask, request, jsonify
from utils import get_not_authorized_response
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user
from dotenv import load_dotenv
import os
from forms import LoginForm, RegisterForm
from flask_bcrypt import Bcrypt
import json
import jwt
import datetime
from functools import wraps

from flask_cors import CORS
import logging

logging.basicConfig(
    format="%(asctime)s:%(levelname)s:% (message)s",
    datefmt="%Y-%m-%d %I:%M:%S%p",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = os.getenv('SECKET_KEY')

db = SQLAlchemy(app=app)

CORS(app=app)
bcrypt = Bcrypt(app=app)
WTF_CSRF_ENABLED = False

# socketio = SocketIO(app, cors_allowed_origins="*")

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


def token_required(key: str = app.config['SECRET_KEY']):
    def wrapper(func):
        @wraps(inner)
        def inner(*args, **kwargs):
            if 'x-access-token' not in request.headers:
                return jsonify({'message': 'token is missing'}, 401)
            
            data = jwt.decode(request.headers['x-access-token'], key, algorithms="HS256")
            user = User.query.filter_by(username=data['username']).first()

            return func(*args, **kwargs)
        return inner
    return wrapper


@app.route('/login', methods=['GET', 'POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return get_not_authorized_response()

    user = User.query.filter_by(username=auth.username).first()

    if not user or not bcrypt.check_password_hash(user.password, auth.password):
        return get_not_authorized_response()

    token = jwt.encode(
        {'username': user.username,
         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    logger.info(token)
    logger.info(jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256"))

    return jsonify({'token': token})


@app.route('/register', methods=['GET', 'POST'])
def register():
    print(request.data)
    print(request.authorization)
    form = RegisterForm()

    if form.password.data == form.password2.data:
        current_user = User.query.filter_by(
            username=form.username.data).first()

        if current_user:
            return json.dumps({'error': 'current username already exists'})

        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

    return json.dumps({'test': 'test'})



# @socketio.on('connect')
# def connection(socket):
#     print('connected with the server')

#     emit('receive_message', {
#         'message': 'hello from the server'
#     })


# @socketio.on('send_message')
# def message(data):
#     print(data)

#     emit('receive_message', {
#         'message': 'hello from the server after receiving from the client'
#     })


if __name__ == '__main__':
    # socketio.run(app, debug=True)
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5001)
