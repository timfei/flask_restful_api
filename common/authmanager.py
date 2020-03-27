from functools import wraps
from flask_restful import request
from flask import g
from common.authErrorHandler import api_abort
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
import config
from resources.users.model import User


# 根据id 生成 token
def generate_token(user):
    expiration = 3600  # 单位秒
    s = Serializer(config.ITS_DANGEROUS_SECRET_KEY, expires_in=expiration)
    token = s.dumps({'id': user.id}).decode('utf-8')
    return token


# 根据 token 获取 user
def validate_token(token):
    s = Serializer(config.ITS_DANGEROUS_SECRET_KEY)
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return False
    user = User.query.get(data['id'])
    if user is None:
        return False
    g.current_user = user  # g 对象每次请求就会重置
    return True


# token 验证装饰器
def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token()
        if request.method != 'OPTIONS':
            if token is None:
                return token_missing()
            if not validate_token(token):
                return invalid_token()
        return f(*args, **kwargs)

    return decorated


# 获取 http 请求 header 中的 token
def get_token():
    if 'token' in request.headers:
        try:
            token = request.headers['token']
        except ValueError:
            token = None
    else:
        token = None
    return token


def invalid_token():
    response = api_abort(401, message='token 过期或无效')
    response.headers['WWW-Authenticate'] = 'Bearer'
    return response


def token_missing():
    response = api_abort(401, message='缺少 token')
    response.headers['WWW-Authenticate'] = 'Bearer'
    return response
