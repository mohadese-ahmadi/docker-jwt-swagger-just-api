from google.oauth2 import id_token
from google.auth.transport import requests

from random import randint

from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.conf import settings

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import Author
from .tokens_storage import reset_tokens


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = Author
        fields = ('username', 'email', 'sex', 'password', 'is_super')


    def create(self, validated_data):
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
        email_input = attrs.get('email')
        token_input = attrs.get('token')

        if email_input not in reset_tokens:
            raise serializers.ValidationError({"email": "No reset request found for this email."})

        token_data = reset_tokens[email_input]

        if str(token_data["token"]) != str(token_input):
            raise serializers.ValidationError({"token": "Invalid token for this email."})

        if timezone.now() > token_data["expires"]:
            reset_tokens.pop(email_input, None)
            raise serializers.ValidationError({"token": "Token expired."})
        return attrs

    def save(self, **kwargs):
        email = self.validated_data["email"]
        new_password = self.validated_data["new_password"]
        user = Author.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        reset_tokens.pop(email, None)
        return user
    
class GoogleAuthSerializer(serializers.Serializer):
    id_token=serializers.CharField(write_only=True)
    access=serializers.CharField(read_only=True)
    refresh=serializers.CharField(read_only=True)
    email=serializers.EmailField(read_only=True)

    def validate_id_token(self, value):
        try:
            info=id_token.verify_oauth2_token(
                value,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
            return info
        except Exception as e:
            raise serializers.ValidationError(f'Invalid Google Token: {e}')
    
    def create(self, validated_data):
        info=validated_data["id_token"]
        email=info['email']
        name=info.get('name', '')

        user, created=Author.objects.get_or_create(email=email)
        if created:
            user.username=email.split('@')[0]
            user.first_name=name
            user.save()

        refresh=RefreshToken.for_user(user)
        return{
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'email': email
        }
