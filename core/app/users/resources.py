from flask.ext.restful import Resource, reqparse
from flask.ext.login import login_required, current_user
from app.users import controllers as user_controllers




class Signup(Resource):
    # post request parser
    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        'name', type=str, required=True, location='json')
    post_parser.add_argument(
        'email', type=str, required=True, location='json')
    post_parser.add_argument(
        'password', type=str, required=True, location='json')
    post_parser.add_argument(
        'profile_url', type=str, required=False, location='json')


    def post(self):
        args = self.post_parser.parse_args()
        return user_controllers.signup(
            args['name'], args['email'], args['password'], args['profile_url'])

    def get(self):
        return {'message' : 'request successful'}


class Login(Resource):
    # post request parser
    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        'email', type=str, required=True, location='json')
    post_parser.add_argument(
        'password', type=str, required=True, location='json')


    def post(self):
        args = self.post_parser.parse_args()
        return user_controllers.login(
            args['email'], args['password'])
