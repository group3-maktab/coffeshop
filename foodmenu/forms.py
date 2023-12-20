from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    parent_name = forms.CharField(label='Parent Category', required=False)

    class Meta:
        model = Category
        fields = ['name', 'parent']

