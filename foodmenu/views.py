from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import AccessMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from functools import wraps
from .forms import CategoryForm
from .utils import json_menu_generator
from .models import Food, Category


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
        return view_func(self, *args, **kwargs)  # another magic here this logic made by me :)

    return _wrapped_view


def is_staff_or_superuser(user):
    return user.is_active and (user.is_staff or user.is_superuser)


class ListFoodView(View):
    template_name = 'Food_ListTemplate.html'
    login_url = 'users:login'

    @staff_or_superuser_required
    def get(self, request):
        menu_data = json_menu_generator()
        return render(request, self.template_name, {'menu_data': menu_data})


class CreateCategoryView(View):
    template_name = 'Food_CreateTemplate.html'

    def get(self, request):
        form = CategoryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('foods:list-food')
        else:
            form = CategoryForm()

        return render(request, 'category_form.html', {'form': form})


class CreateFoodView(View):
    template_name = 'Food_CreateTemplate.html'

    def get(self, request):
        form = CategoryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('foods:list-food')
        else:
            form = CategoryForm()

        return render(request, 'category_form.html', {'form': form})
