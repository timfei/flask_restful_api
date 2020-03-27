from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from flask import jsonify
from .model import User
from app import db
from common import authmanager
from common.authmanager import auth_required
from common.responsepack import generate_resp, RespCode
from common.customErrException import CustomErrException

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'todos': fields.List(fields.Nested({'id': fields.Integer,
                                        'name': fields.String,
                                        'description': fields.String})),
}

user_list_fields = {
    'count': fields.Integer,
    'users': fields.List(fields.Nested(user_fields)),
}

user_post_parser = reqparse.RequestParser(bundle_errors=True)
user_post_parser.add_argument('username', type=str, required=True, location=['json'],
                              help='username required')
user_post_parser.add_argument('password', type=str, required=True, location='json',
                              help='password required')
user_post_parser.add_argument('phone', type=str, required=True, location=['json'],
                              help='phone required')

"""
As of Flask v1.1, the return statement will automatically jsonify a dictionary in the first return value
从 Flask v1.1 开始，请求返回自动 jsonify 不需要 包裹 jsonify() 默认 code = 200 ，如果需要其他 code ， return {'msg': 'Hello world'}, 400
"""


class UserResource(Resource):

    def get(self, user_id=None):
        if user_id > 0:
            user = User.query.filter_by(id=user_id).first()
            return marshal_with(user, user_fields)
        else:
            return jsonify({'msg': 'err'})


class UserLoginResource(Resource):

    def post(self):
        username = request.json['username']
        user = User.query.filter_by(username=username).first()
        if user is not None:
            password = request.json['password']
            if user.password == password:
                token = authmanager.generate_token(user)
                user.token = token
                db.session.commit()
                return generate_resp({'token': token})
            else:
                return generate_resp(None, 'password not correct', RespCode.CODE_ERROR)
        else:
            return generate_resp(None, "register first", RespCode.CODE_ERROR)


class UserRegister(Resource):

    def post(self):
        # password = request.json.get('password')
        # # password = request.json['password']
        # if password is None:
        #     # return {'task': 'Hello world'}
        #     raise CustomErrException(400, 'msg')

        args = user_post_parser.parse_args()
        phone = args.get('phone')
        user = User.query.filter_by(phone=phone).first()
        if user is not None:
            return generate_resp(None, 'user already register', RespCode.CODE_ERROR)
        else:
            user = User(**args)
            db.session.add(user)
            db.session.commit()
            return generate_resp(None, 'user register succeed')


class UserTestResource(Resource):

    @auth_required
    def get(self):
        return jsonify({"msg": "test  succeed"})
