from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import User, ChefProfile
from .forms import UserRegistrationForm, UserUpdateForm, ChefProfileForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('users:login')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if request.user.is_chef:
            chef_form = ChefProfileForm(request.POST, request.FILES, instance=request.user.chefprofile)
            if user_form.is_valid() and chef_form.is_valid():
                user_form.save()
                chef_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('users:profile')
        else:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        if request.user.is_chef:
            chef_form = ChefProfileForm(instance=request.user.chefprofile)
        else:
            chef_form = None
    
    context = {
        'user_form': user_form,
        'chef_form': chef_form
    }
    return render(request, 'users/profile.html', context)
