from http import client

import json


class APIResponse:
    def __init__(self, response: client.HTTPResponse):
        self._response = response
        self._data = json.loads(self._response.read().decode())
        self._code = self._data.pop("code", None)
        self._msg = self._data.pop("msg", None)

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
        self._host = "192.168.13.37"
        self._port = 8000
        self.con = APIHTTPConnection(self._host, self._port)

    def post_request(self, url: str, body=None):
        self.con.request(method="POST", url=url, headers=self._headers, body=body)
        response = self.con.getresponse()
        return response

    def get_request(self, url: str, body=None):
        self.con.request(method="GET", url=url, headers=self._headers, body=body)
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
        print(response.data)
        print(response.code)
        print(response.msg)


    def test(self):
        url = "/user/test/"
        response = self.post_request(url)
        print(response.data)
        print(response.code)
        print(response.msg)


if __name__ == '__main__':
    client = Client()
    # client.register()
    res = client.user_login()

    client.user_logout()
    client.user_logout()
    client.user_logout()
    client.user_logout()
    # client.user_logout()
