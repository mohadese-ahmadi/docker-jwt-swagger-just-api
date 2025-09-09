from django.shortcuts import render

from rest_framework import viewsets

from .models import MenuItem
from .serializers import MenuItemSerializer
from .permissions import IsSuperUserOrReadOnly


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsSuperUserOrReadOnly]
