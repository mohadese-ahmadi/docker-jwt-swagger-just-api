from random import randint
from django.utils import timezone

from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers

from account.models import Author
from .tokens_storage import reset_tokens


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = Author
        fields = ('username', 'email', 'sex', 'password')


    def create(self, validated_data):
        user = Author.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        token_input = attrs.get('token')

        email = None
        for k, v in reset_tokens.items():
            if str(v["token"]) == str(token_input):
                email = k
                break

        if not email:
            raise serializers.ValidationError({"token": "Invalid or unknown token."})

        token_data = reset_tokens[email]
        if timezone.now() > token_data["expires"]:
            reset_tokens.pop(email, None)
            raise serializers.ValidationError({"token": "Token expired."})

        attrs["email"] = email
        return attrs

    def save(self, **kwargs):
        email = self.validated_data["email"]
        new_password = self.validated_data["new_password"]
        user = Author.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        reset_tokens.pop(email, None)
        return user