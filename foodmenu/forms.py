from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.apps import apps

from tag.models import Tag
from .models import Category, Food


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
        }


class FoodCreateForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'flex-row p-2 form-check-input h-100 w-100'}),
        required=False,
    )

    off = forms.IntegerField(max_value=100, min_value=0, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.DecimalField(max_value=10000, min_value=0,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Food
        fields = ['name', 'price', 'off', 'category', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'btn btn-info'}),
        }
