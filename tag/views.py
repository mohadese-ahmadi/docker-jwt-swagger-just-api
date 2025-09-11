from django.shortcuts import render

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from .models import Tags
from .serializers import TagSerializer

@extend_schema(tags=['Tag'])
class TagViewSets(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer