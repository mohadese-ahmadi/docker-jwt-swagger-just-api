from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from random import randint

from drf_spectacular.utils import extend_schema
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from account.models import Author
from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    ResetPasswordRequestSerializer,
    ResetPasswordConfirmSerializer
)

reset_tokens = {}

# ------------------- USER VIEWSET -------------------
class UserViewSet(viewsets.GenericViewSet):
    queryset = Author.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'register':
            from .serializers import RegisterSerializer
            return RegisterSerializer
        elif self.action == 'change_password':
            from .serializers import ChangePasswordSerializer
            return ChangePasswordSerializer
        elif self.action == 'reset_password_request':
            from .serializers import ResetPasswordRequestSerializer
            return ResetPasswordRequestSerializer
        elif self.action == 'reset_password_confirm':
            from .serializers import ResetPasswordConfirmSerializer
            return ResetPasswordConfirmSerializer
        return None

    # ---------------- REGISTER ----------------
    @extend_schema(tags=['register'])
    @action(detail=False, methods=['post'],
             permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # فقط ثبت نام

        # تولید توکن بعد از ثبت نام
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        refresh = str(refresh)

        return Response({
            "user": serializer.data,
            "refresh": refresh,
            "access": access,
        }, status=status.HTTP_201_CREATED)


    # ---------------- CHANGE PASSWORD ----------------
    @extend_schema(tags=['changing password'])
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not check_password(serializer.validated_data["old_password"], user.password):
            return Response({"old_password": "Wrong password."}, status=400)

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"status": "Password updated successfully"})

    # ---------------- RESET PASSWORD REQUEST ----------------
    @extend_schema(tags=['retrieving password'])
    @action(detail=False, methods=['post'], 
            permission_classes=[permissions.AllowAny])
    def reset_password_request(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = Author.objects.get(email=email)
        except Author.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        token = randint(100000, 999999)
        reset_tokens[email] = {"token": token, "expires": datetime.utcnow() + timedelta(minutes=10)}

        send_mail(
            subject="Password Reset",
            message=f"Your reset token is: {token}",
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"status": "Reset email sent. Token valid for 10 minutes."})
    # ---------------- RESET PASSWORD CONFIRM ----------------
    @extend_schema(tags=['retrieving password'])
    @action(detail=False, methods=['post'])
    def reset_password_confirm(self, request):
        user = request.user
        email = request.data.get("email")

        if user.email != email:
            return Response({"error": "Email mismatch"}, status=400)

        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Optionally, you can check reset token here:
        token = request.data.get("token")
        if str(reset_tokens.get(email)) != str(token):
            return Response({"error": "Invalid token"}, status=400)

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        reset_tokens.pop(email, None)

        return Response({"status": "Password reset successful"})

    # ---------------- LOGOUT ----------------
    @extend_schema(tags=['logout'])
    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"},
                            status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token or already blacklisted"},
                            status=status.HTTP_400_BAD_REQUEST)

# ---------------- CUSTOM LOGIN ----------------
@extend_schema(tags=['login'])
class CustomTokenObtainPairView(TokenObtainPairView):
    pass
