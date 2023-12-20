from django import forms
from .models import Category, Food


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']


class FoodCreateForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'price', 'availability', 'off', 'category']
