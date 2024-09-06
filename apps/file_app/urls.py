from django.urls import path, re_path
from apps.file_app import views

urlpatterns = [
    # path('upload/', views.UpAndDownFileGAPIView.as_view(actions={'post': 'post'})),
    # path('upload/', views.UpAndDownFileGAPIView.as_view(actions={'post': 'post'})),
    path('upload/', views.UpAndDownFileGAPIView.as_view()),
    # path('login/', obtain_jwt_token),   # 自带的jwt
]