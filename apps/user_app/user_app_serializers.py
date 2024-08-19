from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from apps.user_app import models
import re


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


    # def create(self, validated_data):
    #
    #     return