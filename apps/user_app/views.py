# Create your views here.
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet, ViewSetMixin
from rest_framework.request import Request
from rest_framework import permissions
from rest_framework import generics
from apps.user_app import user_app_serializers
from apps.user_app import models
from utils.apiresponse import ResponseCode, APIResponse
from rest_framework import views
from rest_framework.authtoken import models as auth_models


# Request._request : HttpRequest
class UserLoginView(ViewSetMixin, generics.GenericAPIView):
    # 使用ViewSetMixin，和APIView要把ViewSetMixin放在前面，因为两---个都有as_view方法，而只有ViewSetMixin中才能输入action参数
    queryset = models.UserModel.objects.all()
    serializer_class = user_app_serializers.LoginModelSerializer

    def post(self, request: Request, *args, **kwargs):
        # 1 需要有个序列化的类
        login_ser = self.get_serializer(data=request.data, context={'request': request})
        # 2 生成序列化类对象
        # 3 调用序列号对象的is_valid
        login_ser.is_valid(raise_exception=False)  # 判断用户是否村子啊啊
        token = login_ser.context.get('token')
        # user = login_ser.context.get('user')
        username = login_ser.context.get('username')
        return APIResponse(code=ResponseCode.SUCCESS, msg="登录成功", token=token, username=username, status=200)


class UserRegisterView(GenericViewSet, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = models.UserModel.objects.all()
    serializer_class = user_app_serializers.UserModelSerializer

    # 假设get请求和post请求，用的序列化类不一样如何处理
    # 重写get_serializer_class方法，返回啥，用的序列化类就是啥
    def get_serializer_class(self):
        if self.action == 'create':
            return super(UserRegisterView, self).get_serializer_class()
        elif self.action == 'retrieve':
            return user_app_serializers.UserReadOnlyModelSerializer
        elif self.action == 'update':
            return user_app_serializers.UserImageModelSerializer


class UserLogoutView(views.APIView):
    permission_classes = permissions.IsAuthenticated,

    def post(self, request, *args, **kwargs):
        # 删除用户的令牌
        try:
            token = auth_models.Token.objects.get(user=request.user)
            token.delete()
        except auth_models.Token.DoesNotExist:
            pass

        # return Response({'status': 200, 'msg': '注销成功'})
        return APIResponse(code=ResponseCode.SUCCESS, msg='注销成功')
