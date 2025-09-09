from rest_framework import generics, permissions, viewsets, views, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Author
from .permissions import IsSuperUserOrReadOnly

from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    ResetPasswordRequestSerializer,
    ResetPasswordConfirmSerializer,
    AuthorSerializer,
)


reset_tokens = {}


class RegisterView(generics.CreateAPIView):
    queryset = Author.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


# ورود: از SimpleJWT -> TokenObtainPairView استفاده می‌کنیم


# خروج: در JWT فقط با بلاک لیست انجام میشه، یا سمت کلاینت توکن پاک شه.


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = Author
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not check_password(serializer.data.get("old_password"), user.password):
                return Response({"old_password": "Wrong password."}, status=400)

            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"status": "Password updated successfully"})
        return Response(serializer.errors, status=400)


class ResetPasswordRequestView(generics.GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = Author.objects.get(email=email)
        except Author.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        token = get_random_string(32)
        reset_tokens[email] = token

        send_mail(
            "Password Reset",
            f"Use this token to reset your password: {token}",
            "no-reply@example.com",
            [email],
        )

        return Response({"status": "Reset email sent."})


class ResetPasswordConfirmView(generics.GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        token = request.data.get("token")
        email = request.data.get("email")

        if reset_tokens.get(email) != token:
            return Response({"error": "Invalid token"}, status=400)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = Author.objects.get(email=email)
        except Author.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        reset_tokens.pop(email)

        return Response({"status": "Password reset successful"})


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token or already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)

    
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsSuperUserOrReadOnly]