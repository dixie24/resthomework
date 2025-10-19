from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.db.models.base import ObjectDoesNotExist 

from .models import ConfirmationCode 
from .serializers import (
    RegisterValidateSerializer, 
    AuthValidateSerializer, 
    ConfirmationSerializer
)


User = get_user_model()


class UserAuthViewSet(GenericViewSet):

    queryset = User.objects.all() 
    
    @action(detail=False, methods=['post'], serializer_class=RegisterValidateSerializer, url_path='register')
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.create(serializer.validated_data) 
        
        return Response(
            status=status.HTTP_201_CREATED, 
            data={
                'user_id': user.id,
                'message': 'User registered. Please use the confirmation code to activate your account.'
            }
        )


    @action(detail=False, methods=['post'], serializer_class=ConfirmationSerializer, url_path='confirm')
    def confirm(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        email = data['email']
        code = data['code']
        
        try:

            user = self.get_queryset().get(email__iexact=email) 

        except ObjectDoesNotExist: 
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
        
        
    @action(detail=False, methods=['post'], serializer_class=AuthValidateSerializer, url_path='authorization')
    def authorization(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.context['user']
        
        token_, created = Token.objects.get_or_create(user=user)
        
        return Response(data={'key': token_.key})