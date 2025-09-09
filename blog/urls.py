from django.urls import path, include
from rest_framework import routers
from .views import BlogViewSets


router=routers.DefaultRouter()
router.register("", BlogViewSets, basename="posts")
urlpatterns=[
    path("", include(router.urls)),
]