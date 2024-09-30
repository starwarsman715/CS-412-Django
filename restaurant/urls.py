from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),            # Handles /restaurant/
    path('main/', views.main, name='main'),       # Handles /restaurant/main/
    path('order/', views.order, name='order'),    # Handles /restaurant/order/
    path('confirmation/', views.confirmation, name='confirmation'),  # Handles /restaurant/confirmation/
]
