from flask import Flask, request_finished, request, url_for, redirect, g
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from sqlalchemy_continuum import make_versioned
import logging
import os


# Creating an instance of app.
app = Flask(__name__)

#Getting settings for the app.
app.config.from_object('settings')

# initailizing a restful api with app.
api = restful.Api(app, prefix='/api')

# # Scheme fix
# app.wsgi_app = ReverseProxied(app.wsgi_app)

# configuring connection with sqlalchemy
db = SQLAlchemy(app)
make_versioned(options={
    'create_models': True,
    'base_classes': (db.Model, ),
    'strategy': 'subquery',
    'transaction_column_name': 'trasaction_id',
    'end_transaction_column_name': 'end_transaction_id',
})


# adding blueprints to app
#from app.tickets import tickets
from app.users import users


app.register_blueprint(users, url_prefix='/api')


if __name__ == '__main__':
    app.run()



# configuring loginmanager
# lm = LoginManager()
# lm.session_protection = None
# lm.init_app(app)

#
# @lm.request_loader
# def load_from_header(request):
#     from app.controllers import lm_controllers
#     if request.method == 'POST' and request.json:
#         if request.json.get('service') and request.json.get(
#                 'signature') and request.json.get('signed'):
#             return lm_controllers.validate_signature(request.json)
#     if request.method == 'POST' and request.form:
#         if request.form.get('service') and request.form.get(
#                 'signature') and request.form.get('signed'):
#             return lm_controllers.validate_signature(request.form)
#     if request.method == 'GET' and request.headers:
#         if request.headers.get('X-Signing-Key'):
#             return lm_controllers.validate_signing_key(
#                 request.headers.get('X-Signing-Key'))
#     redirect(url_for('auth.login'))
#
#
# @lm.user_loader
# def load_user(user_id):
#     from app.models.User import User
#     if not request.cookies.get('sso'):
#         redirect(url_for('auth.login'))
#         return
#     return User.query.filter(User.id == user_id).first()
#
#
# @app.before_request
# def before_request():
#     # Perform cid check for request tagging
#     requests.mutate_with_cid(request.headers, g)
#
#
# @app.after_request
# def add_access_control_headers(response):
#     if response.status_code == 200:
#         if db.session.is_active:
#             db.session.commit()
#     else:
#         db.session.rollback()
#     response.headers[
#         'Access-Control-Allow-Headers'] = 'X-Token,Content-Type'
#     response.headers['Access-Control-Allow-Methods'] = 'POST,GET,PATCH,HEAD'
#     return response
#
