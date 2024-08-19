from django.db import models
from django.contrib.auth.models import AbstractUser
from utils import tool
from apps.user_app import enums


class UserModel(AbstractUser):
    id = models.AutoField(primary_key=True)

    username = models.CharField(max_length=20,
                                null=False,
                                blank=False,
                                verbose_name="用户名",
                                unique=True)
    u_name = models.CharField(max_length=50,
                              null=True,
                              blank=True,
                              default=None,
                              verbose_name="所属人姓名"
                              )
    password = models.CharField(max_length=50,
                                null=False,
                                blank=False,
                                default="123456",
                                verbose_name="密码"
                                )

    gender = models.PositiveSmallIntegerField(
        choices=tool.get_int_choices_enum_choices(enums.UserGender),
        default=enums.UserGender.GN.intvalue,
        null=True,
        blank=True,
        verbose_name="性别"
    )

    is_active = models.BooleanField(
        choices=tool.get_int_choices_enum_choices(enums.UserSignState),
        default=enums.UserSignState.IN,
        null=False,
        blank=False,
        verbose_name="在线状态")

    registration_time = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        verbose_name="注册时间"
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间"
    )

    first_name = None
    email = None
    date_joined = None

    last_name = None
    is_staff = None

    def __str__(self):
        return self.username

    class Meta:
        db_table = "user_app_users"



