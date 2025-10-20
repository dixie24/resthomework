from django.urls import path
from users.views import RegistrationAPIView, AutorizationAPIView, ConfirmationAPIView
#from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView,
# )
# from users.views import CustomTokenObtainPairView
# from users.google_oauth import GoogleLoginAPIView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),

    path('authorization/', AutorizationAPIView.as_view()),
    path('confirm/', ConfirmationAPIView.as_view())

    # path('jwt/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # path('google-login/', GoogleLoginAPIView.as_view()),
]