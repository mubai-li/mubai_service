from django.db import models

# Create your models here.
from enum import Enum, auto


# Create your models here.

# class Permission(models.Model):
#     pass
class Permission(Enum):  # 用户权限
    Admin = auto()
    Election =auto()
    Hot = auto()




class ProjectModel(models.Model):
    pass


class TaskModel(models.Model):
    pass
