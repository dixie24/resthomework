from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ConfirmationCode 
from rest_framework.exceptions import ValidationError


class AuthValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Неверные учетные данные.")
        
        if user.check_password(password):
            if not user.is_active:
                raise serializers.ValidationError("Пользователь не активирован. Подтвердите свой email.")
            self.context['user'] = user
            return data
        
        raise serializers.ValidationError("Неверные учетные данные.")
    
    
class RegisterValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6) 
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            is_active=False
        )
        ConfirmationCode.objects.create(user=user)
        return user 


class ConfirmValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)