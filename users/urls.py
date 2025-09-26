from django.urls import path
from .views import UserAuthViewSet

urlpatterns = [
    path('registration/', UserAuthViewSet.as_view({'post': 'register'})),
    path('authorization/', UserAuthViewSet.as_view({'post': 'authorize'})),
    path('confirm/', UserAuthViewSet.as_view({'post': 'confirm'})),
]
