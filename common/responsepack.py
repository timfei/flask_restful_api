"""
接口成功的返回 json
http status code 都为 200 ，以下的 code 为业务 code
"""


class RespCode:
    CODE_SUCCESS = 1
    CODE_ERROR = 0
    CODE_NO_FOUND = -1

    msg = {
        CODE_SUCCESS: 'success',  # http status code = 200，并且有数据返回，自定义一个业务 code = 1
        CODE_ERROR: 'no data',
        # http status code = 200，业务逻辑出错，没有数据，前台可提示返回的 message，业务 code = 0，这个看业务需求，也可以无数据直接 http status code 400 处理模式
        CODE_NO_FOUND: 'source not found',
    }


def generate_resp(data=None, message=RespCode.msg[RespCode.CODE_SUCCESS], code=RespCode.CODE_SUCCESS):
    return {
        'message': message,
        'status_code': code,
        'data': data
    }
