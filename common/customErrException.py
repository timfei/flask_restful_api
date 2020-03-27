class CustomErrException(Exception):
    # 默认的返回码
    status_code = 400
    message = 'http error'

    def __init__(self, status_code=None, message='error'):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code
            self.message = message

    def to_dict(self):
        return {'code': self.status_code, 'message': self.message}
