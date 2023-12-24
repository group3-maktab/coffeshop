from functools import wraps
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import AppConfig
from django.db.models import Q, Sum, F

from tables.models import Table
from tag.models import TaggedItem, Tag
from django.contrib import messages
from django.db.models import Prefetch, Count
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import random
import os
from twilio.rest import Client
from foodmenu.models import Category, Food
from order.models import Order, OrderItem


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
    categories = (Category.objects.select_related('parent')
                  .prefetch_related(
        Prefetch('subcategories', queryset=Category.objects.select_related('parent')
                 # .exclude(parent_id__in=Category.objects.values_list('id'))
                 .prefetch_related(Prefetch('food_set', queryset=Food.objects.filter(availability=True)))),
        Prefetch('food_set', queryset=Food.objects.filter(availability=True))
    ).filter(Q(parent__isnull=True) | Q(id__in=(Category.objects.values_list('parent_id', flat=True)))))

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

        for food in category.food_set.all():
            category_data['foods'].append({
                'id': food.id,
                'name': food.name,
                'original_price': food.price,
                'off_percent': food.off,
                'price_after_off': food.price_after_off,
            })

        for subcategory in category.subcategories.all():
            if is_parent(subcategory): continue
            subcategory_data = {
                'id': subcategory.id,
                'name': subcategory.name,
                'is_subcategory': subcategory.is_subcategory,
                'foods': []
            }

            for food in subcategory.food_set.all():
                subcategory_data['foods'].append({
                    'id': food.id,
                    'name': food.name,
                    'original_price': food.price,
                    'off_percent': food.off,
                    'price_after_off': food.price_after_off,
                })
            category_data['subcategories'].append(subcategory_data)
        menu.append(category_data)
    return menu


def is_parent(category):
    """
    Check if the category is a parent.
    """
    subcategory_query = Category.objects.select_related('parent').prefetch_related(Prefetch('subcategories',
                                                                                            queryset=Category.objects.select_related(
                                                                                                'parent'))).filter(
        parent=category).exists()
    return subcategory_query or category.parent is None


def staff_or_superuser_required(view_func):
    """
        pecifically, situations where @wraps might be necessary include:

        Decorators for nested functions: When a function is used as a decorator for another function,
         and the latter is defined inside another function (nested functions).

        Usage of decorators in larger codebases:
         In larger projects where multiple decorators are used, employing @wraps helps maintain the proper preservation of metadata for each function, contributing to code organization and readability.

        In essence, using @wraps addresses potential issues related to metadata and leads to better decisions
         for maintaining code and readability.
    """

    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not is_staff_or_superuser(request.user):
            messages.error(request, 'You are not allowed to access this page.')
            return redirect('users:login')
        return view_func(self, request, *args, **kwargs)  # another magic here this logic made by me :)

    return _wrapped_view


def is_staff_or_superuser(user):
    return user.is_active and (user.is_staff or user.is_superuser)


class Authentication:

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_otp_email(to_email):
        otp = Authentication.generate_otp()

        otp_expiry = timezone.now() + timezone.timedelta(minutes=5)

        subject = 'Your verification Code'
        message = f'Your code is: {otp}'

        try:

            email_from = 'djmailyosof@gmail.com'
            recipient_list = [to_email, ]
            send_mail(subject, message, email_from, recipient_list, auth_user=email_from,
                      auth_password=settings.EMAIL_HOST_PASSWORD)
            return otp, otp_expiry
        except Exception as e:
            print(f"Error sending email: {e}")
            return None

    @staticmethod
    def send_otp(phone_number):
        otp = Authentication.generate_otp()
        otp_expiry = timezone.now() + timezone.timedelta(minutes=5)

        account_sid = os.getenv('account_sid')
        auth_token = os.getenv('auth_token')
        twilio_phone_number = os.getenv('twilio_phone_number')

        dist_phone_number = phone_number.replace("0", "+98", 1)

        client = Client(account_sid, auth_token)
        print("Phone Number:", dist_phone_number)
        message = client.messages.create(
            body=f'Your code is: {otp}',
            from_=twilio_phone_number,
            to=dist_phone_number
        )

        print("Twilio Response:", message)
        return otp, otp_expiry

    @staticmethod
    def check_otp(otp, otp_expiry, entered_otp):
        return otp == entered_otp and timezone.now() < otp_expiry


def update_food_availability(changed_tag):
    """
    def update_food_availability(changed_tag):
    tagged_items = TaggedItem.objects.filter(tag=changed_tag)
    food_ids = tagged_items.values_list('object_id', flat=True).distinct()
    related_tags = TaggedItem.objects.filter(object_id__in=food_ids).exclude(tag=changed_tag)
    for food_id in food_ids:
        food = Food.objects.get(id=food_id)
        food_availability = True
        for tag_item in related_tags.filter(object_id=food_id):
            if not tag_item.tag.available:
                food_availability = False
                break
        food.availability = food_availability
        food.save()
    """
    # print('RUN SIGNAL')
    food_ids = TaggedItem.objects.filter(
        tag=changed_tag).values_list(
        'object_id', flat=True).distinct()
    # print('FOOD_IDS:', food_ids)
    food_availability_annotation = (
        TaggedItem.objects
        .filter(object_id__in=food_ids)
        .values('object_id')
        .annotate(unavailable_tags_count=Count(
            'id', filter=models.Q(tag__available=False)))
    )
    # print('FOOD_ANNotate:', food_availability_annotation)
    food_availability_map = {item['object_id']: item['unavailable_tags_count'] for item in
                             food_availability_annotation}
    # print('FOOD_MAP:', food_availability_map)
    for food_id in food_ids:
        food = Food.objects.get(id=food_id)
        # print(food)
        if food_availability_map.get(food_id) and food_availability_map.get(food_id) > 0:
            food.availability = False
        else:
            food.availability = True
        # print(food.availability)
        food.save()


from decimal import Decimal
from django.conf import settings
from foodmenu.models import Food, Category


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """

        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Food.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.
                   cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()


class Reporting:
    """
    Total sales              *
    favorite tables          *
    favorite foods           *
    generate Sales Invoice
    """
    def __init__(self, days):
        self.days = days

    def total_sales(self):
        orders = Order.objects.filter(
            created_at__gte=timezone.now()
                            - timezone.timedelta(days=self.days))

        total_sales = orders.aggregate(
            total_sales=Sum(F('orderitem__price') * F('orderitem__quantity'))
        )
        return total_sales['total_sales']

    def favorite_tables(self):
        most_used_tables = (
            Table.objects
            .annotate(used_seats=Count('order__id', distinct=True, filter=(
                    Q(order__status='F') &
                    Q(order__created_at__gte=timezone.now()
                                             - timezone.timedelta(days=self.days))
            )))
            .order_by('-used_seats')
        )
        for table in most_used_tables:
            yield table
    def favorite_foods(self):
        most_used_foods = (Food.objects.annotate(
            used_foods=Count('orderitem__id', distinct=True, filter=(
                Q(orderitem__created_at__gte=timezone.now()
                  - timezone.timedelta(days=self.days)
                  )
            ))).order_by('-used_foods')[0:10]
        )
        for food in most_used_foods:
            yield food