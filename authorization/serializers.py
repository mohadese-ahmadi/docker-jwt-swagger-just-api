from datetime import datetime

from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from account.models import Author
from .views import reset_tokens 


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Author
        fields = (
            'username', 'email', 'sex',
            'password', 'password2'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': 'Passwords do not match.'
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = Author.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        token_input = attrs.get('token')
        token_data = reset_tokens.get(email)
        if not token_data:
            raise serializers.ValidationError({"token": "No reset request found for this email."})

        if datetime.utcnow() > token_data["expires"]:
            reset_tokens.pop(email, None)
            raise serializers.ValidationError({"token": "Token expired."})

        if str(token_data["token"]) != str(token_input):
            raise serializers.ValidationError({"token": "Invalid token."})

        return attrs

    def save(self, **kwargs):
        email = self.validated_data["email"]
        new_password = self.validated_data["new_password"]
        user = Author.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        reset_tokens.pop(email, None)
        return user


