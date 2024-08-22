from django.utils.deprecation import MiddlewareMixin
from utils.init_redis import encryption_key_cache
from rest_framework.request import Request
from utils.apiresponse import APIResponse, ResponseCode
from mubai_service.settings import caches_time
from enum import Enum, auto

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from utils.BaseClass import AbstractSingleton


class Serialization(AbstractSingleton):
    @classmethod
    def generate_key(cls):
        private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        serialized_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        serialized_public_key = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return serialized_private_key, serialized_public_key

    @classmethod
    def genrate_shared_key(
            cls,
            serialized_private_key,
            serialized_public_key,

    ):
        private_key = serialization.load_pem_private_key(
            serialized_private_key,
            password=None,
            backend=default_backend()
        )
        public_key = serialization.load_pem_public_key(serialized_public_key)
        shared_key = private_key.exchange(ec.ECDH(), public_key)
        return shared_key

    @classmethod
    def genrate_derived_key(cls, shared_key,
                            algorithm=hashes.SHA256(),
                            length=32,
                            salt=None,
                            info=b'handshake data',
                            ):
        derived_key = HKDF(
            algorithm=algorithm,
            length=length,
            salt=salt,
            info=info
        ).derive(shared_key)
        return derived_key

    @classmethod
    def aes_encryption(cls, key, data: str):
        data = data.encode("utf-8")
        iv = "{:0>16}".format(f"{hex(hash(key))}"[2:]).encode("utf-8")
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        ct = encryptor.update(padded_data) + encryptor.finalize()
        return ct

    @classmethod
    def aes_decrypt(cls, key, ct: bytes):
        iv = "{:0>16}".format(f"{hex(hash(key))}"[2:]).encode("utf-8")
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        padded_data = decryptor.update(ct) + decryptor.finalize()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data


class HashesSHA(Enum):
    SHA224 = auto()
    SHA256 = auto()
    SHA384 = auto()
    SHA512 = auto()
    SHA3_224 = auto()
    SHA3_256 = auto()
    SHA3_384 = auto()
    SHA3_512 = auto()
    SHA512_224 = auto()
    SHA512_256 = auto()
    SHAKE128 = auto()
    SHAKE256 = auto()


class DataEncryptionMiddleware(MiddlewareMixin):
    def process_request(self, request: Request):
        print(request.data)
        headers = request.headers

        host = request.META.get('REMOTE_ADDR')
        encryption_key = encryption_key_cache.get(host)
        session_key = headers.get("Session-Key")
        if isinstance(encryption_key,list):
            pass

        elif encryption_key is None and session_key is None:
            # if session_key is None:
            url = request.META.get("PATH_INFO")

            # server_session_key = ec.generate_private_key(ec.SECP256R1()).public_key()
            # public_key = server_session_key.public_bytes(
            #     encoding=serialization.Encoding.PEM,
            #     format=serialization.PublicFormat.SubjectPublicKeyInfo
            # )
            serialized_private_key, serialized_public_key = Serialization.generate_key()

            encryption_key_cache.set(host, serialized_private_key, caches_time)
            headers["Session-Key"] = serialized_public_key
            return APIResponse(ResponseCode.REDIRECTKEY, data={'url': url}, headers=headers)
        elif not isinstance(encryption_key, list) and session_key:
            share_key = Serialization.genrate_shared_key(encryption_key, session_key)

            encryption_key_cache.set(host, [encryption_key, share_key])

            # host_server_encryption_key = serialization.load_pem_public_key(encryption_key)
            # share_key = serialization.load_pem_public_key(session_key)

            # encryption_key_cache.set(host, [session_key, share_key], caches_time)

            # alice_shared_key = alice_private_key.exchange(ec.ECDH(), alice_received_public_key)
            # shared_key = session_key
            # encryption_key_cache.set(host, session_key)

            pass

        # return APIResponse

        # print(headers)
        # print(request.META)

        # print(host)
        # print(dir(request))
        # # encryption_key_cache
        # print(host)
        # print(type(host))
        # print(type(request))

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
