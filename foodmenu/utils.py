from django.db.models import Prefetch
from .models import Category, Food


def json_menu_generator():
    # Fetch all categories with related subcategories and foods
    categories = Category.objects.select_related('parent').prefetch_related(
        Prefetch('subcategories', queryset=Category.objects.select_related('parent')),
        Prefetch('food_set', queryset=Food.objects.filter(availability=True).select_related('category'))
    ).filter(parent__isnull=True)

    menu = []

    for category in categories:
        category_data = {
            'id': category.id,
            'name': category.name,
            'is_subcategory': category.is_subcategory,
            'foods': [],
            'subcategories': []
        }

        # Add foods to the category
        for food in category.food_set.all():
            category_data['foods'].append({
                'id': food.id,
                'name': food.name,
                'original_price': food.price,
                'off_percent': food.off,
                'price_after_off': food.price_after_off,  # Use the price_after_off property here
            })

        # Add subcategories to the category
        for subcategory in category.subcategories.all():
            subcategory_data = {
                'id': subcategory.id,
                'name': subcategory.name,
                'is_subcategory': subcategory.is_subcategory,
                'foods': []
            }

            # Add foods to the subcategory
            for food in subcategory.food_set.all():
                subcategory_data['foods'].append({
                    'id': food.id,
                    'name': food.name,
                    'original_price': food.price,
                    'off_percent': food.off,
                    'price_after_off': food.price_after_off,  # Use the price_after_off property here
                })

            category_data['subcategories'].append(subcategory_data)

        menu.append(category_data)

    return menu
