from app.models.User import User
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app import db
from app import app
from flask.ext.restful import abort
from urllib import quote_plus

def signup(name, email, password, profile_url):
    user = User.query.filter(User.email == func.lower(email)).first()
    if user:
        abort(404, message='Email already registerd !!!')
    user = User()
    user.name = name
    user.email = func.lower(email)
    user.password = password
    user.profile_url = profile_url
    db.session.add(user)
    db.session.commit()
    return {'success': True, 'message': 'Signup successful'}


def login(email, password):
    user = User.query.filter(User.email == func.lower(email)).first()
    if user:
        if user.password == password:
            return {'success': True, 'message': 'Logged in successful'}
        abort(404, message='Wrong password entered')
    abort(404, message='Email is not registerd')
