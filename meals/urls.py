from django.urls import path
from . import views

app_name = 'meals'

urlpatterns = [
    path('', views.dish_list, name='dish_list'),
    path('chef/dashboard/', views.chef_dashboard, name='chef_dashboard'),
    path('chef/dish/add/', views.add_dish, name='add_dish'),
    path('chef/dish/<int:dish_id>/edit/', views.edit_dish, name='edit_dish'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
] 