from flask import jsonify
from werkzeug.exceptions import default_exceptions


def api_abort(code, message=None, **kwargs):
    # 如果 code 为空，且 code 是默认的错误类型，message 为对应描述
    if message is None and code in default_exceptions:
        message = default_exceptions[code].description

    response = jsonify(code=code, message=message, **kwargs)
    response.status_code = code
    return response
