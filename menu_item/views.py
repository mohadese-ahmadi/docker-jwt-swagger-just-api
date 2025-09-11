from django.shortcuts import render

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from .models import MenuItem
from .serializers import MenuItemSerializer
from .permissions import IsSuperUserOrReadOnly

@extend_schema(tags=['Nav Bar'])
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsSuperUserOrReadOnly]
