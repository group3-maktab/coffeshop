from django import forms
from .models import Tag


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['label', 'available']