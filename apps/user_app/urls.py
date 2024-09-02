from django.urls import path, re_path

from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token
from apps.user_app import views
# from django.utils.encoding import smart_text
# from django.utils import encoding
# encoding.smart_str()
from mubai_service import settings

router = SimpleRouter()
router.register('register', views.UserRegisterView, 'register')

urlpatterns = [
    path('login/', views.UserLoginView.as_view(actions={'post': 'post'})),
    # path('login/', obtain_jwt_token),   # 自带的jwt
]
urlpatterns.extend(router.urls)

if not settings.JWTToken:
    urlpatterns.append(
        path('logout/', views.UserLogoutView.as_view()),

    )
