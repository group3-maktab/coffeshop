from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import AccessMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from .forms import CategoryForm
from .utils import json_menu_generator
from .models import Food, Category


def is_staff_or_superuser(user):
    return user.is_active and (user.is_staff or user.is_superuser)
# @user_passes_test(is_staff_or_superuser, login_url='users:login')


class ListFoodView(AccessMixin, View):
    template_name = 'Food_ListTemplate.html'
    login_url = 'users:login'

    def get(self, request):
        if not self.request.user or not is_staff_or_superuser(self.request.user):
            messages.error(request, 'You are not allowed to this page')
            return self.handle_no_permission()

        menu_data = json_menu_generator()
        return render(request, self.template_name, {'menu_data': menu_data})



class CreateFoodView(View):
    pass


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

