from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Dish, Order, Subscription, Review
from .forms import DishForm
from django.contrib.auth.models import User
from django.db.models import Q

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
    if request.user.is_chef:
        subscriptions = Subscription.objects.filter(chef=request.user)
    else:
        subscriptions = Subscription.objects.filter(customer=request.user)
    return render(request, 'meals/subscription_list.html', {'subscriptions': subscriptions})

@login_required
def subscription_detail(request, subscription_id):
    if request.user.is_chef:
        subscription = get_object_or_404(Subscription, id=subscription_id, chef=request.user)
    else:
        subscription = get_object_or_404(Subscription, id=subscription_id, customer=request.user)
    return render(request, 'meals/subscription_detail.html', {'subscription': subscription})

@login_required
def create_subscription(request):
    if request.method == 'POST':
        chef_id = request.POST.get('chef')
        chef = get_object_or_404(User, id=chef_id, is_chef=True)
        plan_name = request.POST.get('plan_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        subscription = Subscription.objects.create(
            customer=request.user,
            chef=chef,
            plan_name=plan_name,
            start_date=start_date,
            end_date=end_date,
            status='pending'
        )
        messages.success(request, 'Subscription created successfully!')
        return redirect('meals:subscription_detail', subscription_id=subscription.id)
    return render(request, 'meals/subscription_form.html')

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
