from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from apps.user_app import models
import re
from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ("username", "u_name", "password", "gender", "is_active")

    def validate(self, data):
        email = data.get('email')
        if email:
            if not self.is_valid_email(email):
                raise serializers.ValidationError({"email": "Invalid email format"})
        return data

    def is_valid_email(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def create(self, validated_data):
        # models.User.objects.create(**validated_data)  # 这个密码不会加密
        user = models.UserModel.objects.create_user(**validated_data)
        return user


class UserReadOnlyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        # fields = '__all__'
        fields = ['username', 'icon']


class UserImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ['icon']


class LoginModelSerializer(serializers.ModelSerializer):
    username = serializers.CharField()  # 因为我们需要处理username，且不想让model里面的user对象处理username参数所以需要这么写，不写的话会使用的django自己的校验

    class Meta:
        model = models.UserModel
        fields = ['username', 'password']

    def validate(self, attrs):
        # 在这里写逻辑
        username = attrs.get('username')  # 用户名有三种方式
        password = attrs.get('password')
        # 通过判断username数据不同，查询字段不一样来判断是什么类型的数据，其实也可以添加一个字段直接在前段判断提交方式来判断
        if re.match('^1[3-9]\d{9}$', username):
            user = models.User.objects.filter(mobile=username).first()
        elif re.match('^.*@.*\.com$', username):
            user = models.UserModel.objects.filter(email=username).first()
        else:
            user = models.UserModel.objects.filter(username=username).first()
        if user:
            # 校验密码,因为是密文，要用check_password
            if user.check_password(password):
                # 签发token
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                self.context['token'] = token
                self.context['username'] = username
                return attrs
            else:
                raise ValidationError('密码错误')

        raise ValidationError('用户不存在')
