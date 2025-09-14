from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    RegisterView,
    ChangePasswordView,
    ResetPasswordRequestView,
    ResetPasswordConfirmView,
    LogoutView,
    CustomTokenObtainPairView
)

router = DefaultRouter()

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("reset-password/", ResetPasswordRequestView.as_view(), name="reset_password"), #forgotten password
    path("reset-password/confirm/", ResetPasswordConfirmView.as_view(), name="reset_password_confirm"),
]
