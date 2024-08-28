from django.urls import path, re_path

from apps.user_app import views

urlpatterns = [
    path('user/login/', views.UserLogin.as_view()),
    path('user/register/', views.UserRegister.as_view()),
]
