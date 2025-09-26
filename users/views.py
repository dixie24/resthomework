# users/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .serializers import (
    RegisterValidateSerializer, 
    AuthValidateSerializer, 
    ConfirmValidateSerializer
)
from .models import ConfirmationCode 
@api_view(['POST'])
def registration_api_view(request):
    serializer = RegisterValidateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'errors': serializer.errors})

    validated_data = serializer.validated_data

    user = User.objects.create_user(
        username=validated_data['username'],
        password=validated_data['password'],
        email=validated_data.get('email'), 
        is_active=False
    )

    conf_code_entry = ConfirmationCode.objects.create(user=user)
    
    return Response(
        status=status.HTTP_201_CREATED, 
        data={
            'user_id': user.id,
            'message': 'User registered. Please use the confirmation code to activate your account.'
        }
    )


@api_view(['POST'])
def confirmation_api_view(request):
    serializer = ConfirmValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    data = serializer.validated_data
    email = data['email']
    code = data['code']
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'User not found!'})
    
    if user.is_active:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'User already active!'})
    try: 
        conf_entry = ConfirmationCode.objects.get(user=user, code=code)
    except ConfirmationCode.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid confirmation code!'})
    
    user.is_active = True
    user.save()
    conf_entry.delete() 
    
    return Response(status=status.HTTP_200_OK, 
                    data={'message': 'User successfully confirmed and activated!'})

@api_view(['POST'])
def authorization_api_view(request):
    serializer = AuthValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    
    user = authenticate(username=username, password=password)

    if user is not None:
        if not user.is_active:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED, 
                data={'error': 'Account not active. Please confirm your email.'}
            )
        
        token_, created = Token.objects.get_or_create(user=user)
        
        return Response(data={'key': token_.key})
        
    return Response(
        status=status.HTTP_401_UNAUTHORIZED,
        data={'error': 'Invalid credentials.'}
    )