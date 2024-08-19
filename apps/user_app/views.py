from django.shortcuts import render
from rest_framework import generics
from django.http.request import HttpRequest
from django.http.response import HttpResponse


from rest_framework.response import Response
from rest_framework.request import Request
# Create your views here.
from apps.user_app import models
from apps.user_app import user_app_serializers
from django.utils.decorators import method_decorator
# Request._request : HttpRequest

class UserView(generics.GenericAPIView):
    queryset = models.UserModel.objects
    serializer_class = user_app_serializers.UserModelSerializer

    def get(self, request: Request, *args, **kwargs):

        # print(request.auth)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        # print(x_forwarded_for)
        # print(request.get_host)
        # print(request._request.get_host())
        # print(request.get_port())
        # print(request._request.META)
        # print(request._request.META.get('HTTP_X_FORWARDED_FOR'))
        # print(request._request.META.get('REMOTE_ADDR'))  # 获取客户端的ip用来做服务通信
        # print(request.user)

        return Response("1")


    def post(self, request: Request, *args, **kwargs):
        print(request.data)
        # print(request.DATA)
        # pass
        # user_ser: user_app_serializers.UserModelSerializer = self.get_serializer(date=request.data)
        # # user_ser =  user_app_serializers.UserModelSerializer(data=request.data)
        #
        #
        #
        # if user_ser.is_valid():
        #     user_ser.save()
        #     return Response()
        return Response("")
