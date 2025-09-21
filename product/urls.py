from django.urls import path
from . import views


urlpatterns = [
    path('', views.product_cud_api_view),
    path('<int:id>/', views.product_detail_api_view),    
]