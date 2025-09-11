from django.shortcuts import render

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from .models import Category
from .serializers import CategorySerializer

@extend_schema(tags=['Category'])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer