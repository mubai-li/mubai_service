from django.urls import path,re_path

from apps.user_app import views
urlpatterns = [
    path('test/',views.UserView.as_view()),

]
