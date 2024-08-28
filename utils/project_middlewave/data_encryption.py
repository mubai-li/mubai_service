import json

from django.utils.deprecation import MiddlewareMixin
from utils.init_redis import encryption_key_cache
from rest_framework.response import Response
from utils.apiresponse import APIResponse, ResponseCode
from mubai_service.settings import caches_time
from enum import Enum, auto
import hashlib
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec

from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from utils.BaseClass import AbstractSingleton
from django.core.handlers.wsgi import WSGIRequest
import base64


class Serialization(AbstractSingleton):
    @classmethod
    def generate_key(cls) -> tuple[bytes, bytes]:
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

    ) -> bytes:
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
                            ) -> bytes:
        derived_key = HKDF(
            algorithm=algorithm,
            length=length,
            salt=salt,
            info=info
        ).derive(shared_key)
        return derived_key

    @classmethod
    def aes_encryption(cls, key, data: str) ->bytes:
        data = data.encode("utf-8")
        sha256 = hashlib.sha256()
        sha256.update(key)
        hash_value = sha256.digest()
        iv = hash_value[:16]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        ct = encryptor.update(padded_data) + encryptor.finalize()
        return ct

    @classmethod
    def aes_decrypt(cls, key, ct: bytes) -> bytes:
        sha256 = hashlib.sha256()
        sha256.update(key)
        hash_value = sha256.digest()
        iv = hash_value[:16]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        padded_data = decryptor.update(ct) + decryptor.finalize()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data

    @classmethod
    def b85_decode(cls, key: bytes) -> str:
        return base64.b85encode(key).decode()

    @classmethod
    def b85_encode(cls, key: str) -> bytes:
        return base64.b85decode(key)


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
    def process_request(self, request: WSGIRequest):
        json_data = json.loads(request.body.decode())

        session_data = json_data.get("session_data")
        headers = request.headers

        host = request.META.get('REMOTE_ADDR')
        encryption_key = encryption_key_cache.get(host)
        session_key = headers.get("Session-Key")
        if isinstance(encryption_key, list):
            if session_data:
                share_key = encryption_key[1]
                data = Serialization.aes_decrypt(share_key, Serialization.b85_encode(session_data))
                json_data["session_data"] = data
                request._body = json.dumps(json_data)
                return
            else:
                return

        elif encryption_key is None:

            url = request.META.get("PATH_INFO")

            serialized_private_key, serialized_public_key = Serialization.generate_key()

            encryption_key_cache.set(host, serialized_private_key, caches_time)
            headers["Session-Key"] = Serialization.b85_decode(serialized_public_key)
            return APIResponse(ResponseCode.REDIRECTKEY, data={'url': url}, headers=headers)
        elif not isinstance(encryption_key, list) and session_key:
            # 存储并解密
            share_key = Serialization.genrate_shared_key(encryption_key, session_key)
            encryption_key_cache.set(host, [encryption_key, share_key])
            if session_data is not None:
                data = Serialization.aes_decrypt(share_key, Serialization.b85_encode(session_data))
                json_data["session_data"] = data
                request._body = json.dumps(json_data)
            return
        return

    def process_response(self, request, response: Response):
        session_data = response.data.get("session_data")
        if session_data is None:
            return None
        host = request.META.get('REMOTE_ADDR')
        encryption_key = encryption_key_cache.get(host)
        headers = request.headers
        session_key = headers.get("Session-Key")
        if isinstance(encryption_key, list):
            if session_data:
                share_key = encryption_key[1]
                data = Serialization.aes_encryption(share_key, json.dumps(session_data))
                response.data["session_data"] = Serialization.b85_decode(data)
            return response
        elif encryption_key is None:
            url = request.META.get("PATH_INFO")
            serialized_private_key, serialized_public_key = Serialization.generate_key()
            encryption_key_cache.set(host, serialized_private_key, caches_time)
            headers["Session-Key"] = Serialization.b85_decode(serialized_public_key)
            return APIResponse(ResponseCode.REDIRECTKEY, data={'url': url}, headers=headers)
        elif not isinstance(encryption_key, list) and session_key:
            share_key = Serialization.genrate_shared_key(encryption_key, session_key)
            encryption_key_cache.set(host, [encryption_key, share_key])
            if session_data is not None:
                data = Serialization.aes_encryption(share_key, json.dumps(session_data))
                response.data["session_data"] = Serialization.b85_decode(data)
            return response
        return response
