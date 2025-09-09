from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSets

router = DefaultRouter()
router.register("", BlogViewSets, basename="posts")

urlpatterns = [
    path("", include(router.urls)),
]