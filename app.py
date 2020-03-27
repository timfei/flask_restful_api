from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.exceptions import default_exceptions
# from common.customErrException import CustomErrException

import config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['BUNDLE_ERRORS'] = True

# init db
db = SQLAlchemy(app)

# init marshmallow
ma = Marshmallow(app)

# init restful api
api = Api(app)
api.prefix = '/api'


# 捕获未知的各类错误
@app.errorhandler(Exception)
def handle_error(error):
    error_info = '{} error'.format(error)
    response = jsonify({'code': 404, 'message': error_info, 'data': None})
    response.status_code = 404
    return response


# # 自定义的异常捕获，用于接口需要返回 http status cod 400 等
# @app.errorhandler(CustomErrException)
# def handle_custom_error(error):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response


for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)

# for ex in default_exceptions:
#     app.register_error_handler(ex, handle_custom_error)

from resources.users.resource import UserRegister
from resources.users.resource import UserResource
from resources.users.resource import UserLoginResource
from resources.users.resource import UserTestResource

api.add_resource(UserRegister, '/register', endpoint='register')
api.add_resource(UserResource, '/user', endpoint='userresource')
api.add_resource(UserLoginResource, '/login', endpoint='userreloginsource')
api.add_resource(UserTestResource, '/test', endpoint='usertestresource')

if __name__ == '__main__':
    app.run(debug=True)
