from django.shortcuts import render, get_object_or_404
from .models import Dish, Order
from django.contrib import messages

def home(request):
    featured_dishes = Dish.objects.filter(is_featured=True)[:6]
    context = {'featured_dishes': featured_dishes}
    return render(request, 'home.html', context)

def dish_list(request):
    dishes = Dish.objects.all()
    return render(request, 'meals/dish_list.html', {'dishes': dishes})

def dish_detail(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    return render(request, 'meals/dish_detail.html', {'dish': dish})

def checkout(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    return render(request, 'meals/checkout.html', {'dish': dish})

def payment_success(request):
    messages.success(request, "Payment successful! Thank you for your order.")
    return render(request, 'meals/payment_success.html')

# Custom error handlers
def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
