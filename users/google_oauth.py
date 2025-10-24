import os
import requests
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from users.serializers import OauthCodeSerializer
from rest_framework import status
from django.db import transaction
from django.utils import timezone


User = get_user_model()

class GoogleLoginAPIView(CreateAPIView):
    serializer_class = OauthCodeSerializer
    authentication_classes = [] 
    permission_classes = [] 

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data["code"]

        try:
            token_response = requests.post(
                url="https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                    "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                    "redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI"),
                    "grant_type": "authorization_code",
                },
            )
            token_response.raise_for_status() # Вызовет исключение для 4xx/5xx ошибок
            token_data = token_response.json()
            access_token = token_data.get("access_token")

            if not access_token:
                return Response({"error": "Invalid token response from Google."}, status=status.HTTP_400_BAD_REQUEST)
        
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to exchange code for token: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_info_response = requests.get(
                url="https://www.googleapis.com/oauth2/v3/userinfo",
                params={"alt": "json"},
                headers={"Authorization": f"Bearer {access_token}"},
            )
            user_info_response.raise_for_status()
            user_info = user_info_response.json()
            print(f"user_info {user_info}")

            email = user_info.get("email")
            given_name = user_info.get("given_name", "") 
            family_name = user_info.get("family_name", "")

            if not email:
                 return Response({"error": "Email not provided by Google."}, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
             return Response({"error": f"Failed to get user info: {e}"}, status=status.HTTP_400_BAD_REQUEST)


        with transaction.atomic():
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email,
                    'first_name': given_name,
                    'last_name': family_name,
                    'is_active': True,
                    'date_joined': timezone.now(), 
                    'last_login': timezone.now(), 
                }
            )

            if not created:
                user.first_name = given_name
                user.last_name = family_name
                user.is_active = True
                user.last_login = timezone.now()
                user.save()

            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email

            return Response(
                {"access_token": str(refresh.access_token), "refresh_token": str(refresh)},
                status=status.HTTP_200_OK
            )