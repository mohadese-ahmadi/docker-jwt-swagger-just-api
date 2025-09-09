from django.urls import path, include
from .views import TagViewSets
from rest_framework.routers import DefaultRouter
router=DefaultRouter()

router.register('', TagViewSets , basename='tag' )
urlpatterns=[
    path('', include(router.urls))
]