from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    ChangePasswordView,
    ResetPasswordRequestView,
    ResetPasswordConfirmView,
    LogoutView,
    AuthorViewSet
)
router=DefaultRouter()
router.register('author', AuthorViewSet , basename='author')
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name='logout'),
    #path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("reset-password/", ResetPasswordRequestView.as_view(), name="reset_password"), #forgotten password
    #path("reset-password/confirm/", ResetPasswordConfirmView.as_view(), name="reset_password_confirm"),
    path('', include(router.urls))
]
