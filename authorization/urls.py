from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GoogleAuthViewSet, UserViewSet

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('google-login', GoogleAuthViewSet, basename='google-login')

urlpatterns = [
    path("", include(router.urls)),
]
