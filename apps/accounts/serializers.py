"""
Serializers for authentication and user management.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'phone',
                  'password', 'password_confirm']
        read_only_fields = ['id']

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username', validated_data['email'].split('@')[0]),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            password=validated_data['password'],
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile (read/update)."""
    full_name = serializers.ReadOnlyField()
    total_orders = serializers.SerializerMethodField()
    total_spent = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'full_name',
                  'phone', 'avatar', 'address', 'city', 'postal_code', 'country',
                  'date_of_birth', 'date_joined', 'total_orders', 'total_spent']
        read_only_fields = ['id', 'email', 'date_joined']

    def get_total_orders(self, obj):
        return obj.orders.count() if hasattr(obj, 'orders') else 0

    def get_total_spent(self, obj):
        if hasattr(obj, 'orders'):
            from django.db.models import Sum
            result = obj.orders.filter(status__in=['delivered', 'shipped']).aggregate(
                total=Sum('total_amount')
            )
            return float(result['total'] or 0)
        return 0


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for admin user listing."""
    full_name = serializers.ReadOnlyField()
    total_orders = serializers.SerializerMethodField()
    total_spent = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone', 'role', 'is_active',
                  'date_joined', 'total_orders', 'total_spent']

    def get_total_orders(self, obj):
        return obj.orders.count() if hasattr(obj, 'orders') else 0

    def get_total_spent(self, obj):
        if hasattr(obj, 'orders'):
            from django.db.models import Sum
            result = obj.orders.filter(status__in=['delivered', 'shipped']).aggregate(
                total=Sum('total_amount')
            )
            return float(result['total'] or 0)
        return 0


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value


class AdminUserSerializer(serializers.ModelSerializer):
    """Serializer for admin user management (settings/users)."""

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name',
                  'role', 'is_active', 'is_staff', 'date_joined']
        read_only_fields = ['id', 'date_joined']
