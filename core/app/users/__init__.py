from flask import Blueprint
from flask.ext import restful

users = Blueprint('users', __name__)

api = restful.Api(users)

# add resources to api.
from app.users.resources import (Signup, Login)
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
