from django.test import TestCase

# Create your tests here.
import os
from mubai_service import settings

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings.__name__)
    import django
    import sys

    django.setup()

    from rest_framework.routers import SimpleRouter

    from apps.user_app import views

    router = SimpleRouter()
    router.register('register', views.UserRegisterView, 'register')

    print(router.routes)
    print(router.urls)