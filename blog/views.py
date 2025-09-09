from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import BlogSerializer
from .models import Blogs
from .permissions import IsAuthorOrReadOnly


class BlogViewSets(viewsets.ModelViewSet):
    queryset = Blogs.objects.all().order_by("created_at")
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)