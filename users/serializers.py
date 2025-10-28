from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import ConfirmationCode
from users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from django.core.cache import cache


class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    phone_number = serializers.CharField(max_length=15)
    

class AuthValidateSerializer(UserBaseSerializer):
    pass


class RegisterValidateSerializer(UserBaseSerializer):
    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise ValidationError('Email уже существует!')

class ConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        input_code = attrs.get('code')
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise ValidationError('User не существует!')

        cache_key = f"confirmation_code_{user_id}"
        stored_code = cache.get(cache_key)
        
        if stored_code is None:
            raise ValidationError('Код подтверждения не найден или истёк!')
        
        if stored_code != input_code: 
            raise ValidationError('Неверный код подтверждения!')

        cache.delete(cache_key)
        user.is_active = True
        user.save()
        
        return attrs

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user) 
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        if user.birthdate:
            token['birthdate'] = user.birthdate.isoformat() 
        else:
            token['birthdate'] = None

        return token

class OauthCodeSerializer(serializers.Serializer):
    code = serializers.CharField()