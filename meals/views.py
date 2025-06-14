from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Dish, Order, Subscription, Review
from .forms import DishForm, SubscriptionForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

def dish_list(request):
    dishes = Dish.objects.filter(is_available=True)
    return render(request, 'meals/dish_list.html', {'dishes': dishes})

def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id, is_available=True)
    return render(request, 'meals/dish_detail.html', {'dish': dish})

@login_required
def order_list(request):
    if request.user.is_chef:
        orders = Order.objects.filter(dish__chef=request.user)
    else:
        orders = Order.objects.filter(customer=request.user)
    return render(request, 'meals/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    if request.user.is_chef:
        order = get_object_or_404(Order, id=order_id, dish__chef=request.user)
    else:
        order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'meals/order_detail.html', {'order': order})

@login_required
def create_order(request):
    dish_id = request.GET.get('dish')
    dish = get_object_or_404(Dish, id=dish_id, is_available=True)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        delivery_address = request.POST.get('delivery_address', request.user.location)
        delivery_time = request.POST.get('delivery_time')
        order = Order.objects.create(
            customer=request.user,
            dish=dish,
            quantity=quantity,
            delivery_address=delivery_address,
            delivery_time=delivery_time,
        )
        messages.success(request, 'Order placed successfully!')
        return redirect('meals:order_detail', order_id=order.id)
    return render(request, 'meals/order_form.html', {'dish': dish})

@login_required
def chef_dashboard(request):
    if not request.user.is_chef:
        return redirect('home')
    
    dishes = Dish.objects.filter(chef=request.user)
    orders = Order.objects.filter(dish__chef=request.user)
    subscriptions = Subscription.objects.filter(chef=request.user)
    
    return render(request, 'meals/chef_dashboard.html', {
        'dishes': dishes,
        'orders': orders,
        'subscriptions': subscriptions
    })

@login_required
def customer_dashboard(request):
    if request.user.is_chef:
        return redirect('meals:chef_dashboard')
    orders = Order.objects.filter(customer=request.user)
    subscriptions = Subscription.objects.filter(customer=request.user)
    return render(request, 'meals/customer_dashboard.html', {'orders': orders, 'subscriptions': subscriptions})

@login_required
def add_dish(request):
    if not request.user.is_chef:
        return redirect('home')
    
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            dish = form.save(commit=False)
            dish.chef = request.user
            dish.save()
            messages.success(request, 'Dish added successfully!')
            return redirect('meals:chef_dashboard')
    else:
        form = DishForm()
    
    return render(request, 'meals/dish_form.html', {
        'form': form,
        'title': 'Add New Dish'
    })

@login_required
def edit_dish(request, dish_id):
    if not request.user.is_chef:
        return redirect('home')
    
    dish = get_object_or_404(Dish, id=dish_id, chef=request.user)
    
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dish updated successfully!')
            return redirect('meals:chef_dashboard')
    else:
        form = DishForm(instance=dish)
    
    return render(request, 'meals/dish_form.html', {
        'form': form,
        'title': 'Edit Dish'
    })

def home(request):
    featured_dishes = Dish.objects.filter(is_featured=True)[:6]
    context = {
        'featured_dishes': featured_dishes
    }
    return render(request, 'home.html', context)

@login_required
def subscription_list(request):
    subscriptions = Subscription.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'meals/subscription_list.html', {'subscriptions': subscriptions})

@login_required
def subscription_detail(request, subscription_id):
    if request.user.is_chef:
        subscription = get_object_or_404(Subscription, id=subscription_id, chef=request.user)
        template = 'meals/chef_subscription_detail.html'
    else:
        subscription = get_object_or_404(Subscription, id=subscription_id, customer=request.user)
        template = 'meals/customer_subscription_detail.html'
    return render(request, template, {'subscription': subscription})

@login_required
def create_subscription(request, chef_id):
    chef = get_object_or_404(User, id=chef_id, is_chef=True)
    
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.customer = request.user
            subscription.chef = chef
            subscription.save()
            messages.success(request, 'Subscription created successfully!')
            return redirect('meals:subscription_detail', subscription_id=subscription.id)
    else:
        form = SubscriptionForm()
    
    return render(request, 'meals/subscription_form.html', {
        'form': form,
        'chef': chef
    })

@login_required
def cancel_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id, customer=request.user)
    
    if subscription.is_active:
        subscription.status = 'cancelled'
        subscription.save()
        messages.success(request, 'Subscription cancelled successfully!')
    else:
        messages.error(request, 'Cannot cancel this subscription.')
    
    return redirect('meals:subscription_detail', subscription_id=subscription.id)

@login_required
def review_list(request):
    if request.user.is_chef:
        reviews = Review.objects.filter(dish__chef=request.user)
    else:
        reviews = Review.objects.filter(customer=request.user)
    return render(request, 'meals/review_list.html', {'reviews': reviews})

@login_required
def create_review(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        review = Review.objects.create(
            customer=request.user,
            dish=dish,
            rating=rating,
            comment=comment
        )
        messages.success(request, 'Review submitted successfully!')
        return redirect('meals:dish_detail', dish_id=dish.id)
    return render(request, 'meals/review_form.html', {'dish': dish})

def search_results(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Dish.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_available=True
        )
    return render(request, 'meals/search_results.html', {'query': query, 'results': results})

def filter_results(request):
    is_veg = request.GET.get('is_veg')
    is_available = request.GET.get('is_available')
    dishes = Dish.objects.all()
    if is_veg in ['true', 'false']:
        dishes = dishes.filter(is_veg=(is_veg == 'true'))
    if is_available in ['true', 'false']:
        dishes = dishes.filter(is_available=(is_available == 'true'))
    return render(request, 'meals/filter_results.html', {'dishes': dishes})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully!')
    else:
        messages.error(request, 'Cannot cancel this order.')
    return redirect('meals:order_detail', order_id=order.id)

@login_required
def chef_orders(request):
    if not request.user.is_chef:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('meals:dish_list')
    
    orders = Order.objects.filter(dish__chef=request.user).order_by('-created_at')
    return render(request, 'meals/chef_orders.html', {'orders': orders})

@login_required
def update_order_status(request, order_id):
    if not request.user.is_chef:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('meals:dish_list')
    
    order = get_object_or_404(Order, id=order_id, dish__chef=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order status updated to {order.get_status_display()}.')
        else:
            messages.error(request, 'Invalid status.')
    
    return redirect('meals:chef_orders')

def chef_list(request):
    chefs = User.objects.filter(is_chef=True)
    return render(request, 'meals/chef_list.html', {'chefs': chefs})

@login_required
def chef_subscriptions(request):
    if not request.user.is_chef:
        messages.error(request, 'You must be a chef to access this page.')
        return redirect('meals:chef_dashboard')
    
    subscriptions = Subscription.objects.filter(chef=request.user).order_by('-created_at')
    active_subscriptions = subscriptions.filter(status='active')
    cancelled_subscriptions = subscriptions.filter(status='cancelled')
    expired_subscriptions = subscriptions.filter(status='expired')
    
    context = {
        'active_subscriptions': active_subscriptions,
        'cancelled_subscriptions': cancelled_subscriptions,
        'expired_subscriptions': expired_subscriptions,
        'total_subscribers': active_subscriptions.count(),
        'total_revenue': sum(sub.total_price for sub in active_subscriptions),
    }
    return render(request, 'meals/chef_subscriptions.html', context)

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
