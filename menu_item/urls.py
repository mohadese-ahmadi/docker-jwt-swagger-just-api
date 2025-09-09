from django.urls import path, include
from .views import MenuItemViewSet
from rest_framework.routers import DefaultRouter
router=DefaultRouter()

router.register('', MenuItemViewSet , basename='menu' )
urlpatterns=[
    path('', include(router.urls))
]