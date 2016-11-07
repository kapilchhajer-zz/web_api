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
