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


class FoodCreateForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Food
        fields = ['name', 'price', 'off', 'category', 'tags']

