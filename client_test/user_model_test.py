import copy
import os.path
from codecs import encode
from http import client
import mimetypes
import json

import requests
from client_test.util import _encode_files


class APIResponse:
    def __init__(self, response: client.HTTPResponse):
        self._response = response
        data = self._response.read().decode()

        if self.status == 200:
            self._data = json.loads(data)
            self._code = self._data.pop("code", None)
            self._msg = self._data.pop("msg", None)

        else:
            self._data = data
            self._code = None
            self._msg = None

    @property
    def data(self):
        return self._data

    @property
    def headers(self):
        return self._response.headers

    @property
    def status(self):
        return self._response.status

    @property
    def code(self):
        return self._code

    @property
    def msg(self):
        return self._msg

    @property
    def response(self):
        return self._response


class APIHTTPConnection(client.HTTPConnection):
    def getresponse(self) -> APIResponse:
        response = super().getresponse()
        aip_response = APIResponse(response)
        return aip_response


# def get_response


class Client:
    JWTToken = True

    def __init__(self):
        self._username = "mubai"
        self._password = "lb12345678@"
        self._headers = {
            "Content-Type": "application/json"
        }
        # self._host = "172.23.80.150"
        # self._host = "192.168.13.37"
        # self._host = "192.168.12.130"
        self._host = "127.0.0.1"
        self._port = 8000
        self.con = APIHTTPConnection(self._host, self._port)

    def post_request(self, url: str, body=None, headers=None):
        if headers is None:
            headers = self._headers
        self.con.request(method="POST", url=url, headers=headers, body=body)
        response = self.con.getresponse()
        return response

    def get_request(self, url: str, body=None, headers=None):
        if headers is None:
            headers = self._headers
        self.con.request(method="GET", url=url, headers=headers, body=body)
        response = self.con.getresponse()
        return response

    def register(self):
        url = "/user/register/"
        body = {
            "username": self._username,
            "password": self._password,

            "u_name": "柏",

            "gender": 1

        }
        response = self.post_request(url, json.dumps(body))
        print(response.data)

        return response

    def user_login(self):
        url = "/user/login/"
        body = {
            "username": self._username,
            "password": self._password
        }
        response = self.post_request(url, json.dumps(body))
        token = response.data.get('token')
        if self.JWTToken:
            self._headers["Authorization"] = f'JWT {token}'
        else:
            self._headers["Authorization"] = f'Token {token}'
        return response

    def user_logout(self):
        url = "/user/logout/"
        response = self.post_request(url)

    def upload_file(self, file_path: str):
        url = "/file/file/"
        header = copy.copy(self._headers)
        with open(file_path, 'rb') as f:
            file_content = f.read()
            body = {os.path.basename(file_path): file_content}

            body, content_type = _encode_files(body, {})
            header["Content-Type"] = content_type
            response = self.post_request(url, body=body, headers=header)

        return response

    def add_file_type(self, file_type):
        url = "/file/type/"
        self.post_request(url, body=json.dumps(file_type))

    def add_file_label(self, file_type):
        url = "/file/label/"
        self.post_request(url, body=json.dumps(file_type))


if __name__ == '__main__':
    Client.JWTToken = True
    client = Client()
    # client.register()
    res = client.user_login()
    # res = client.upload_file(r"C:\Users\32509\Desktop\Project\日月新\002+006图纸及表格数据-20240511.rar")

    # client.add_file_type({
    #     "file_type": "file",
    #     "file_type_remark": "1"
    # })
    # client.add_file_label({
    #     "": ""
    # })
    # print(res.headers)
    print(client._headers)

    # client.user_logout()

    #