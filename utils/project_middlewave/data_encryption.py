from django.utils.deprecation import MiddlewareMixin
from utils.init_redis import encryption_key_cache
from rest_framework.request import Request
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization

from utils.apiresponse import APIResponse, ResponseCode


class DataEncryptionMiddleware(MiddlewareMixin):
    def process_request(self, request: Request):
        headers = request.headers

        # print(request.META)
        # session_key  = headers.get(s)
        host = request.META.get('REMOTE_ADDR')
        encryption_key = encryption_key_cache.get(host)
        if encryption_key is None:
            session_key = headers.get("Session-Key")
            if session_key is None:
                server_session_key = ec.generate_private_key(ec.SECP256R1())




        url = request.META.get("PATH_INFO")

        # print(headers)
        # print(request.META)

        print(host)
        print(dir(request))
        # encryption_key_cache
        print(host)
        print(type(host))
        print(type(request))

        # if encryption_key is None:
        #     user_server_key = ec.generate_private_key(ec.SECP256R1())

        # if encryption_key is None:
        #     pass
        # else:
        #     pass
        # pass
        # print(encryption_key)
        # request.user
        # if encryption_key_cache.get(host)
        # pass
        # csrf_token = self._get_token(request)
        # if csrf_token is not None:
        # Use same token next time.x
        # request.META['CSRF_COOKIE'] = csrf_token
        # return HttpResponseRedirect(redirect(url))

    # def process_view(self, request, callback, callback_args, callback_kwargs):
    #     print(dir(request))
    # return request

    def process_response(self, request, response):
        return response
