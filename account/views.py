from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, viewsets, views, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

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


@extend_schema(tags=['register'])
class RegisterView(generics.CreateAPIView):
    queryset = Author.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


# ورود: از SimpleJWT -> TokenObtainPairView استفاده می‌کنیم
# خروج: در JWT فقط با بلاک لیست انجام میشه، یا سمت کلاینت توکن پاک شه.


@extend_schema(tags=['changing password'])
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


@extend_schema(tags=['retrieving password'])
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
            subject="Password Reset",
            message=f"Use this token to reset your password: {token}",
            from_email=None,  # Uses DEFAULT_FROM_EMAIL if set
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"status": "Reset email sent."})


@extend_schema(tags=['retrieving password'])
class ResetPasswordConfirmView(generics.GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        email = request.data.get("email")

        if user.email != email:
            return Response({"error": "Email mismatch"}, status=400)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response({"status": "Password reset successful"})


@extend_schema(tags=['logout'])
class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"},
                             status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token or already blacklisted"},
                             status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['login'])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=['users '])
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsSuperUserOrReadOnly]