from django.urls import path
from . import views

urlpatterns = [
    path('', views.dish_list, name='dish_list'),
    path('<int:pk>/', views.dish_detail, name='dish_detail'),
    path('<int:dish_id>/checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
]
