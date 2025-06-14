from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ChefProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    location = forms.CharField(max_length=100)
    is_chef = forms.BooleanField(required=False, label='Register as a Chef')

    class Meta:
        model = User
        fields = ['username', 'email', 'location', 'is_chef', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    location = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'location']

class ChefProfileForm(forms.ModelForm):
    class Meta:
        model = ChefProfile
        fields = ['bio', 'specialization', 'experience_years', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        } 