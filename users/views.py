from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import User, ChefProfile
from .forms import UserRegistrationForm, ChefProfileForm, UserUpdateForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_chef:
                ChefProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('home')
    return render(request, 'users/logout.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if request.user.is_chef:
            p_form = ChefProfileForm(request.POST, request.FILES, instance=request.user.chef_profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('users:profile')
        else:
            if u_form.is_valid():
                u_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        if request.user.is_chef:
            p_form = ChefProfileForm(instance=request.user.chef_profile)
            context = {
                'u_form': u_form,
                'p_form': p_form
            }
        else:
            context = {
                'u_form': u_form
            }
    return render(request, 'users/profile.html', context)
