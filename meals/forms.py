from django import forms
from .models import Dish

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'image', 'is_veg', 'is_available', 'is_featured', 'expiry_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'expiry_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        } 