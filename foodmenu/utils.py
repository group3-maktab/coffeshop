from django.db.models import Prefetch
from .models import Category, Food


def json_menu_generator():
    """
    https://docs.djangoproject.com/en/5.0/ref/models/querysets/

    select_related works by creating an SQL join and including the fields of the related object in the SELECT statement.
     For this reason, select_related gets the related objects in the same database query.
      However, to avoid the much larger result set that would result from joining across a ‘many’ relationship,
       select_related is limited to single-valued relationships - foreign key and one-to-one.

    prefetch_related, on the other hand, does a separate lookup for each relationship,
     and does the ‘joining’ in Python. This allows it to prefetch many-to-many,
      many-to-one, and GenericRelation objects which cannot be done using select_related,
       in addition to the foreign key and one-to-one relationships that are supported by select_related.
        It also supports prefetching of GenericForeignKey, however,
         the queryset for each ContentType must be provided in the querysets parameter of GenericPrefetch.
    """
    # Fetch all categories with related subcategories and foods
    """
    prefetch_related in most cases will be implemented using an SQL query that
     uses the ‘IN’ operator. 
     This means that for a large QuerySet a large ‘IN’ clause could be generated,
      which, depending on the database,
       might have performance problems of its own when it comes to
        parsing or executing the SQL query. Always profile for your use case!

If you use iterator() to run the query,
 prefetch_related() calls will only be observed if a value for chunk_size is provided.

You can use the Prefetch object to further control the prefetch operation.
    """
    categories = Category.objects.select_related('parent').prefetch_related(
        Prefetch('subcategories', queryset=Category.objects.select_related('parent')),
        Prefetch('food_set', queryset=Food.objects.filter(availability=True).select_related('category'))
    ).filter(parent__isnull=True)
    """
    this code will generate:) Absolute Magic ->
    """
    """
    SELECT 
    "foodmenu_category"."id" AS "category_id",
    "foodmenu_category"."name" AS "category_name",
    "foodmenu_category"."parent_id" AS "category_parent_id",
    "parent_category"."id" AS "parent_id",
    "parent_category"."name" AS "parent_name",
    "subcategory"."id" AS "subcategory_id",
    "subcategory"."name" AS "subcategory_name",
    "foodmenu_food"."id" AS "food_id",
    "foodmenu_food"."name" AS "food_name",
    "foodmenu_food"."price" AS "food_price",
    "foodmenu_food"."availability" AS "food_availability",
    "foodmenu_food"."off" AS "food_off",
    "foodmenu_food"."category_id" AS "food_category_id"
    FROM "foodmenu_category"
    LEFT OUTER JOIN "foodmenu_category" AS "parent_category" ON ("foodmenu_category"."parent_id" = "parent_category"."id")
    LEFT OUTER JOIN "foodmenu_category" AS "subcategory" ON ("foodmenu_category"."id" = "subcategory"."parent_id")
    LEFT OUTER JOIN "foodmenu_food" ON ("foodmenu_category"."id" = "foodmenu_food"."category_id" AND "foodmenu_food"."availability" = True)
    WHERE "foodmenu_category"."parent_id" IS NULL;
    """


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
                'price_after_off': food.price_after_off,
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
