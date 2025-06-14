from django import forms
from .models import Dish, Review, Subscription
from django.utils import timezone

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'image', 'is_veg', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['plan', 'start_date', 'end_date', 'meals_per_week', 'price_per_meal']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        meals_per_week = cleaned_data.get('meals_per_week')
        price_per_meal = cleaned_data.get('price_per_meal')

        if start_date and end_date:
            if start_date < timezone.now().date():
                raise forms.ValidationError("Start date cannot be in the past")
            if end_date <= start_date:
                raise forms.ValidationError("End date must be after start date")
            if (end_date - start_date).days < 7:
                raise forms.ValidationError("Subscription must be at least 1 week long")

        if meals_per_week and meals_per_week > 14:
            raise forms.ValidationError("Maximum 14 meals per week allowed")

        if price_per_meal and price_per_meal <= 0:
            raise forms.ValidationError("Price per meal must be greater than 0")

        return cleaned_data 