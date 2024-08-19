from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
# Create your views here.
from apps.user_app import models
from apps.user_app import user_app_serializers


class UserView(generics.GenericAPIView):
    queryset = models.User.objects
    serializer_class = user_app_serializers.UserModelSerializer

    def post(self, request, *args, **kwargs):
        user_ser: user_app_serializers.UserModelSerializer = self.get_serializer(date=request.data)
        # user_ser =  user_app_serializers.UserModelSerializer(data=request.data)
        if user_ser.is_valid():
            user_ser.save()
            return Response()