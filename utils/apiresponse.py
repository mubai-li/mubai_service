from rest_framework.response import Response
from enum import Enum, auto


class ResponseCode(Enum):
    SUCCESS = auto()  # 成功
    ERROR = auto()  # 报错
    REDIRECT = auto()  # 重定向报错
    REDIRECTKEY = auto()  # 重定向秘钥
    PERMISSION = auto()  # 权限报错


class APIResponse(Response):
    def __init__(
            self,
            code: ResponseCode = ResponseCode.SUCCESS,
            msg='成功',
            data=None,
            session_data=None,
            status=None,
            headers=None,
            exception=False,
            content_type=None,
            **kwargs):
        dic = {
            'code': code.value,
            'msg': msg,
        }
        if data: dic['data'] = data
        if session_data: dic['session_data'] = data
        dic.update(kwargs)
        super(APIResponse, self).__init__(
            data=dic,
            status=status,
            headers=headers,
            exception=exception,
            content_type=content_type)
