from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Food, Category

def food_list(request):
    # Get all Food items
    foods = Food.objects.all()

    # Get all parent categories (categories with no parent)
    parent_categories = Category.objects.filter(parent__isnull=True)

    # Get all subcategories
    subcategories = Category.objects.filter(parent__isnull=False)

    # Pass the data to the template
    context = {
        'foods': foods,
        'parent_categories': parent_categories,
        'subcategories': subcategories
    }
    return render(request, '', context)