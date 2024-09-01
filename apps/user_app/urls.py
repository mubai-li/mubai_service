from django.urls import path, re_path

from rest_framework.routers import SimpleRouter

from apps.user_app import views

router = SimpleRouter()
router.register('register', views.UserRegisterView, 'register')
urlpatterns = [
    path('login/', views.UserLoginView.as_view(actions={'post': 'post'})),
    path('logout/', views.LogoutView.as_view()),
]
urlpatterns.extend(router.urls)
