# users/serializers.py
from .models import CustomUser
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

# Serializer for creating a new user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user

# Serializer for token authentication (Login)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = CustomUser.objects.filter(username=data['username']).first()
        if user and user.check_password(data['password']):
            refresh = RefreshToken.for_user(user)
            return {'refresh': str(refresh), 'access': str(refresh.access_token)}
        raise serializers.ValidationError('Invalid credentials')
