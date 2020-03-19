from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
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
