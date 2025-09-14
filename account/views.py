from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from .models import Author
from .permissions import IsSuperUserOrReadOnly
from .serializers import (
    AuthorSerializer
)


@extend_schema(tags=['users '])
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsSuperUserOrReadOnly]