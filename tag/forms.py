# forms.py
from django import forms
from .models import Tag


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['label', 'available']

    label = forms.CharField(label="label", widget=forms.TextInput(attrs={'class': 'form-control'}))
    available = forms.BooleanField(label="available",required=False , widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))