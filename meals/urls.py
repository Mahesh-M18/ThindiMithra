from django.urls import path
from . import views

app_name = 'meals'

urlpatterns = [
    path('dishes/', views.dish_list, name='dish_list'),
    path('dish/<int:dish_id>/', views.dish_detail, name='dish_detail'),
    path('chef/dashboard/', views.chef_dashboard, name='chef_dashboard'),
    path('chef/dish/add/', views.add_dish, name='add_dish'),
    path('chef/dish/<int:dish_id>/edit/', views.edit_dish, name='edit_dish'),
    path('chef/orders/', views.chef_orders, name='chef_orders'),
    path('chef/orders/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/<int:order_id>/cancel/', views.cancel_order, name='order_cancel'),
    path('subscriptions/', views.subscription_list, name='subscription_list'),
    path('subscriptions/<int:subscription_id>/', views.subscription_detail, name='subscription_detail'),
    path('subscriptions/<int:subscription_id>/cancel/', views.cancel_subscription, name='cancel_subscription'),
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/create/<int:dish_id>/', views.create_review, name='create_review'),
    path('search/', views.search_results, name='search_results'),
    path('filter/', views.filter_results, name='filter_results'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('chefs/', views.chef_list, name='chef_list'),
    path('chefs/<int:chef_id>/subscribe/', views.create_subscription, name='create_subscription'),
    path('chef/subscriptions/', views.chef_subscriptions, name='chef_subscriptions'),
] 