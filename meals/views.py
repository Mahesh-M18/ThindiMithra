from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Dish, Order, Subscription
from .forms import DishForm

def dish_list(request):
    dishes = Dish.objects.filter(is_available=True)
    return render(request, 'meals/dish_list.html', {'dishes': dishes})

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
        return redirect('home')
    
    orders = Order.objects.filter(customer=request.user)
    subscriptions = Subscription.objects.filter(customer=request.user)
    
    return render(request, 'meals/customer_dashboard.html', {
        'orders': orders,
        'subscriptions': subscriptions
    })

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
