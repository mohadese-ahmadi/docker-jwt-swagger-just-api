from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id', 'username', 'email', 'first_name',
            'last_name', 'sex', 'is_superuser'
        ]
        read_only_fields = ['id', 'is_superuser']
