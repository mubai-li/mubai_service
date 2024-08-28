from django.shortcuts import render
from rest_framework import generics
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from utils.apiresponse import APIResponse
from rest_framework.response import Response
from rest_framework.request import Request
# Create your views here.
from apps.user_app import models
from apps.user_app import user_app_serializers
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings


# Request._request : HttpRequest


class UserLogin(generics.GenericAPIView):
    queryset = models.UserModel.objects.all()
    serializer_class = user_app_serializers.UserModelSerializer

    def get(self, request, *args, **kwargs):
        return APIResponse(data=1)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            return APIResponse(meg='Logged in successfully')
        else:
            return APIResponse(msg='Invalid credentials')


class UserRegister(generics.GenericAPIView):
    queryset = models.UserModel.objects
    serializer_class = user_app_serializers.UserModelSerializer

    def get(self, request: Request, *args, **kwargs):
        return APIResponse(data=1)

    def post(self, request: Request, *args, **kwargs):
        return APIResponse(data="123")
