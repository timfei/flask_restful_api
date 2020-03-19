from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from flask import jsonify
from .model import User
from app import db
from common import authmanager

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

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('username', type=str, required=True, location=['json'],
                              help='username required')
user_post_parser.add_argument('password', type=str, required=True, location=['json'],
                              help='password required')
user_post_parser.add_argument('phone', type=int, required=True, location=['json'],
                              help='password required')


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
                return jsonify({'msg': 'password is  correct', 'token': token})
            else:
                return jsonify({'msg': 'password is not correct'})
        else:
            return jsonify({'msg': 'register first'})


class UserRegister(Resource):

    def post(self):
        args = user_post_parser.parse_args()
        phone = args.get('phone')
        user = User.query.filter_by(phone=phone).first()
        if user is not None:
            return jsonify({'msg': 'user already register'})
        else:
            user = User(**args)
            db.session.add(user)
            db.session.commit()
            return jsonify({'msg': 'user register succeed'})


class UserTestResource(Resource):

    @authmanager.auth_required
    def get(self):
        return jsonify({"msg": "user auth succeed"})
