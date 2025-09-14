from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("", include(router.urls)),
]
