from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import TagViewSets

router = DefaultRouter()
router.register('', TagViewSets, basename='tag')

urlpatterns = [
    path('', include(router.urls))
]