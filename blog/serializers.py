from rest_framework import serializers
from .models import Blogs

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = [
            'id',
            'title',
            'description',
            'context',
            'category',
            'tag',
            'image_file']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be blank.")
        return value

    def validate_content(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Content is too short.")
        return value