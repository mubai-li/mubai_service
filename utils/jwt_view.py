# from rest_framework.authentication import BaseAuthentication
from rest_framework_jwt.authentication import BaseAuthentication, BaseJSONWebTokenAuthentication
from rest_framework import exceptions
import jwt
from rest_framework_jwt.utils import jwt_decode_handler
from django.contrib.auth import get_user_model
from rest_framework_jwt.utils import jwt_get_username_from_payload_handler
# from api import models


def my_jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'msg': '成功',
        'status': 100,
        'username': user.username
    }


class MyJwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print('HTTP_Authorization'.upper())
        jwt_value = request.META.get('HTTP_AUTHORIZATION')
        # jwt_value = request.META.get('HTTP_JWT'.upper())

        if jwt_value:
            # jwt提供了通过三段token，取出payload的方法，并且具有校验功能
            ...
            try:
                payload = jwt_decode_handler(jwt_value)
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('签名过期')
            except jwt.InvalidTokenError:
                raise exceptions.AuthenticationFailed('非法用户')
            except Exception as e:
                raise exceptions.AuthenticationFailed(str(e))
            # 得到user对象
            # 第一种去数据库查
            # user = models.User.objects.filter(pk=payload.get('user_id'))
            # return (user,payload)
            # 第二种不查库
            # user =  models.User(id=payload.get('user_id'),username=payload.get("username"))
            # 第三种使用django内置的方法，其实也可以通过继承BaseJSONWebTokenAuthentication来直接使用
            user = get_user_model()
            username = jwt_get_username_from_payload_handler(payload)
            user = user.objects.get_by_natural_key(username)
            return (user, payload)
        else:
            raise exceptions.AuthenticationFailed('你未携带认证信息')


class MyJwtAuthentication1(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        print('HTTP_Authorization'.upper())
        jwt_value = request.META.get('HTTP_AUTHORIZATION')
        # jwt_value = request.META.get('HTTP_JWT'.upper())

        if jwt_value:
            # jwt提供了通过三段token，取出payload的方法，并且具有校验功能
            ...
            try:
                payload = jwt_decode_handler(jwt_value)
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('签名过期')
            except jwt.InvalidTokenError:
                raise exceptions.AuthenticationFailed('非法用户')
            except Exception as e:
                raise exceptions.AuthenticationFailed(str(e))
            user = self.authenticate_credentials(payload)
            return (user, payload)
        else:
            raise exceptions.AuthenticationFailed('你未携带认证信息')