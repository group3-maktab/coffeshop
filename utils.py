import csv
from abc import ABC,abstractmethod
from collections import namedtuple
from datetime import timedelta
from functools import wraps
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import models
from django.db.models.functions import ExtractHour, Extract, ExtractWeekDay
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import AppConfig
from django.db.models import Q, Sum, F, ExpressionWrapper, DecimalField
from django.http import HttpResponse

from tables.models import Table
from tag.models import TaggedItem, Tag
from django.contrib import messages
from django.db.models import Prefetch, Count
from django.shortcuts import redirect, get_object_or_404
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
    https://docs.djangoproject.com/en/5.0/ref/models/querysets/.....

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


class StaffSuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


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
        self.session = request.session  # todo expire at 30 M
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
                                     'price': str(product.price_after_off)}
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

    def edit_orders(self, order_id):
        self.cart.clear()
        products = OrderItem.objects.filter(order_id=order_id)
        for product in products:
            self.add(product=product.product,
                     quantity=product.quantity,
                     override_quantity=True)
        order = Order.objects.get(pk=order_id)
        order.status = "C"
        order.save()


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
        """
        By using ExpressionWrapper in combination with annotate or other queryset methods,
         you can include more complex database expressions in your queries,
          providing flexibility and allowing you to perform calculations directly at the database level.
        """
        # def total_sales(self):
        #     orders = Order.objects.filter(
        #         created_at__gte=timezone.now()
        #                         - timezone.timedelta(days=self.days),status__in=["F"])
        #
        #     total_sales = orders.aggregate(
        #         total_sales=Sum(F('items__price_after_off') * F('items__quantity'))
        #     )
        #     return total_sales['total_sales']

        orders = Order.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=self.days),
            status='F'
        )

        total_sales = orders.aggregate(
            total_sales=Sum(
                F('items__price') * F('items__quantity'),
            )
        )

        return total_sales['total_sales']

    def favorite_tables(self):
        most_used_tables = (
            Table.objects
            .annotate(used_seats=Count('orders__id', distinct=True, filter=(
                    Q(orders__status='F') &
                    Q(orders__created_at__gte=timezone.now()
                                              - timezone.timedelta(days=self.days))
            )))
            .order_by('-used_seats')
        )
        for table in most_used_tables:
            yield table

    def favorite_foods(self):
        """
        collections.namedtuple is a factory function in Python's collections module that creates
         a new class with named fields. It returns a new class type that can be used to create tuples
          with named fields.
        used namedtuple to create a simple data structure (FoodData) to represent
         the data for each food item with named fields. This makes it easier to manage and access
          the attributes in the template.
        """
        FoodData = namedtuple('FoodData', ['id', 'name', 'total_sales', 'counts', 'category'])

        most_used_foods = (
            Food.objects
            .filter(
                orderitem__order__created_at__gte=timezone.now() - timezone.timedelta(days=self.days),
                orderitem__order__status='F'
            )
            .annotate(
                used_foods=Sum('orderitem__quantity', distinct=True),
                total_sales=Sum(
                    F('orderitem__quantity') * F('orderitem__price'),
                )
            )
            .select_related('category')
            .order_by('-used_foods')
        )

        for food in most_used_foods:
            if food.used_foods > 0:
                food_data = FoodData(
                    id=food.pk,
                    name=food.name,
                    total_sales=food.total_sales,
                    counts=food.used_foods,
                    category=food.category,
                )
                yield food_data

    def get_percentage_difference(self):
        """
        Calculate the percentage difference between the current time frame and the previous one.
        For instance, if self.days is 2, it will compare the last 2 days with the 2 days before that.
        """
        current_sales = self.total_sales()
        previous_days_sales = Reporting(self.days * 2).total_sales()
        if previous_days_sales:
            percentage_difference = ((current_sales - previous_days_sales) / previous_days_sales) * 100
        else:
            percentage_difference = 0

        return percentage_difference

    def peak_hours(self):  # todo: Dahanam sevice shod :-|
        start_hour = 0
        end_hour = 24

        orders = Order.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=self.days),
            status='F'
        )

        orders_by_hour = orders.annotate(hour=ExtractHour('created_at'))

        peak_hours_data = (
            orders_by_hour
            .filter(hour__gte=start_hour, hour__lt=end_hour)
            .values('hour')
            .annotate(order_count=Count('id'))
            .order_by('-order_count')
        )

        peak_hours_list = []
        for hour_data in peak_hours_data:
            current_hour = hour_data['hour']
            next_hour = current_hour + 1 if current_hour < 23 else 0  # 24th hour wraps back to 0 #todo: ajab shizi shod :-)

            order_count = hour_data['order_count']
            peak_hours_list.append({
                'hour_range': f"{current_hour} - {next_hour}",
                'order_count': order_count
            })
        if peak_hours_list:
            return peak_hours_list, list(peak_hours_list[0].values())[0]
        else:
            return 'No hour found', 'No hour found'

    def peak_day_of_week(self):

        orders = Order.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=self.days),
            status='F'
        )

        orders_by_day = orders.annotate(day_of_week=ExtractWeekDay('created_at'))

        peak_days_data = (
            orders_by_day
            .values('day_of_week')
            .annotate(order_count=Count('id'))
            .order_by('-order_count')
        )

        peak_days_list = []
        for day_data in peak_days_data:
            day_of_week = day_data['day_of_week']
            order_count = day_data['order_count']
            peak_days_list.append({
                'day_of_week': day_of_week,
                'order_count': order_count
            })
        if peak_days_list:
            return peak_days_list
        else:
            return None

    def best_cutomer(self):
        orders = Order.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=self.days),
            status='F'
        )
        best_customer_data = (
            orders
            .values('customer_phone')
            .annotate(order_count=Count('id'))
            .order_by('-order_count')
        )
        if best_customer_data:
            return list(best_customer_data[0].values())[0]
        else:
            return 'No user found'

    def favorite_category(self):
        CategoryData = namedtuple('CategoryData', ['id', 'name', 'total_sales'])

        most_used_categories = (
            Category.objects
            .filter(
                food__orderitem__order__created_at__gte=timezone.now() - timezone.timedelta(days=self.days),
                food__orderitem__order__status='F'
            )
            .annotate(
                total_sales=Sum(
                    F('food__orderitem__quantity') * F('food__orderitem__price'),
                )
            )
            .order_by('-total_sales')
        )

        for category in most_used_categories:
            if category.total_sales > 0:
                category_data = CategoryData(
                    id=category.pk,
                    name=category.name,
                    total_sales=category.total_sales,
                )
                yield category_data


class CSVExportMixin(StaffSuperuserRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if 'export_csv' in request.GET:
            queryset = self.get_csv_export_queryset()
            filename = self.get_csv_export_filename()
            return self.export_csv(queryset, filename)

        return super().dispatch(request, *args, **kwargs)

    def get_csv_export_queryset(self):
        return None

    def get_csv_export_filename(self):
        return 'exported_data'

    def export_csv(self, queryset, filename):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

        writer = csv.writer(response)
        headers = [field.name for field in queryset.model._meta.fields]
        writer.writerow(headers)

        for obj in queryset:
            writer.writerow([str(getattr(obj, field)) for field in headers])

        return response
