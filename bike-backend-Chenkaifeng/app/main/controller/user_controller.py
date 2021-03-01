from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user, check_user_password

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user


@api.route('/register')
class UserRegister(Resource):
    @api.doc('To register a user.')
    def post(self):
        data = request.get_json()
        print(data)
        if ("firstname" not in data or "lastname" not in data):
            return {
                'status': 'fail',
                'message': 'Firstname and Lastname are required.',
            }, 409
        return save_new_user(data=data)


@api.route('/login')
class UserLogin(Resource):
    @api.doc('To login with user name or email')
    def post(self):
        data = request.get_json()
        return check_user_password(data=data)
