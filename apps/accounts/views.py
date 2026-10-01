"""
Views for authentication and user management.
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema

from apps.core.permissions import IsAdminUser
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    UserListSerializer,
    ChangePasswordSerializer,
    AdminUserSerializer,
)

User = get_user_model()


@extend_schema(tags=['Auth'])
class RegisterView(generics.CreateAPIView):
    """Register a new customer account."""
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Auth'])
class ProfileView(generics.RetrieveUpdateAPIView):
    """Get or update the authenticated user's profile."""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=['Auth'])
class ChangePasswordView(APIView):
    """Change password for authenticated user."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Auth'])
class LogoutView(APIView):
    """Logout by blacklisting the refresh token."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


# ─── Admin Views ────────────────────────────────────────────────────────────

@extend_schema(tags=['Auth'])
class AdminUserListView(generics.ListCreateAPIView):
    """Admin: List all users or create a new admin user."""
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    filterset_fields = ['role', 'is_active']
    search_fields = ['email', 'first_name', 'last_name', 'phone']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdminUserSerializer
        return UserListSerializer


@extend_schema(tags=['Auth'])
class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Get, update, or delete a user."""
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]


@extend_schema(tags=['Auth'])
class CustomerListView(generics.ListAPIView):
    """Admin: List all customers with order stats."""
    queryset = User.objects.filter(role='customer')
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    filterset_fields = ['is_active']
