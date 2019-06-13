from django.urls import path
from apps.users.views import register_user
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('register/', register_user, name="register_user"),
    path('login/', obtain_jwt_token, name="login_user"),
]
