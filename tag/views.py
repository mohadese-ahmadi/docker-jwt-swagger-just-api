from django.shortcuts import render
from rest_framework import viewsets
from .models import Tags
from .serializers import TagSerializer
# Create your views here.
class TagViewSets(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer