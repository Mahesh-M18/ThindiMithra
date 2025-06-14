from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ChefProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    location = forms.CharField(max_length=100, required=True)
    user_type = forms.ChoiceField(
        choices=[('customer', 'Customer'), ('chef', 'Chef')],
        widget=forms.RadioSelect,
        required=True,
        label='I want to sign up as a'
    )
    
    # Chef-specific fields
    specialization = forms.CharField(max_length=100, required=False)
    experience_years = forms.IntegerField(min_value=0, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'location', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        
        if user_type == 'chef':
            specialization = cleaned_data.get('specialization')
            experience_years = cleaned_data.get('experience_years')
            
            if not specialization:
                self.add_error('specialization', 'Specialization is required for chefs')
            if experience_years is None:
                self.add_error('experience_years', 'Years of experience is required for chefs')
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.location = self.cleaned_data['location']
        
        if self.cleaned_data['user_type'] == 'chef':
            user.is_chef = True
        
        if commit:
            user.save()
            
            # Create chef profile if user is a chef
            if user.is_chef:
                ChefProfile.objects.create(
                    user=user,
                    specialization=self.cleaned_data['specialization'],
                    experience_years=self.cleaned_data['experience_years'],
                    profile_picture=self.cleaned_data.get('profile_picture')
                )
        
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    location = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'location']

class ChefProfileForm(forms.ModelForm):
    class Meta:
        model = ChefProfile
        fields = ['bio', 'specialization', 'experience_years', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        } 