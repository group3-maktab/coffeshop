from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import CategoryCreateForm, FoodCreateForm
from utils import json_menu_generator, staff_or_superuser_required
from .models import Food, Category
from django.db.models.deletion import ProtectedError



class ListFoodView(View):
    template_name = 'Food_ListTemplate.html'
    login_url = 'users:login'

    @staff_or_superuser_required
    def get(self, request):
        menu_data = json_menu_generator()
        return render(request, self.template_name, {'menu_data': menu_data})


class CreateCategoryView(View):
    template_name = 'Food_CreateCategoryTemplate.html'

    @staff_or_superuser_required
    def get(self, request):
        form = FoodCreateForm()
        return render(request, self.template_name, {'form': form})

    @staff_or_superuser_required
    def post(self, request):
        form = FoodCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('foods:list-food')
        else:
            form = CategoryCreateForm()

        return render(request, 'category_form.html', {'form': form})


class CreateFoodView(View):
    template_name = 'Food_CreateFoodTemplate.html'

    @staff_or_superuser_required
    def get(self, request):
        form = FoodCreateForm()
        return render(request, self.template_name, {'form': form})

    @staff_or_superuser_required
    def post(self, request):
        form = FoodCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food created successfully!')
            return redirect('foods:list-food')
        else:
            form = FoodCreateForm()

        return render(request, 'category_form.html', {'form': form})


class UpdateFoodView(View):
    template_name = 'Food_CreateFoodTemplate.html'

    @staff_or_superuser_required
    def get(self, request, pk):
        food_object = Food.objects.get(pk=pk)
        form = FoodCreateForm(instance=food_object)
        return render(request, self.template_name, {'form': form})

    @staff_or_superuser_required
    def post(self, request, pk):
        food_object = Food.objects.get(pk=pk)
        form = FoodCreateForm(request.POST, instance=food_object)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food updated successfully!')
            return redirect('foods:list-food')

        return render(request, 'category_form.html', {'form': form})


class UpdateCategoryView(View):
    template_name = 'Food_CreateCategoryTemplate.html'

    @staff_or_superuser_required
    def get(self, request, pk):
        category_object = Category.objects.get(pk=pk)
        form = CategoryCreateForm(instance=category_object)
        return render(request, self.template_name, {'form': form})

    @staff_or_superuser_required
    def post(self, request, pk):
        category_object = Category.objects.get(pk=pk)
        form = CategoryCreateForm(request.POST, instance=category_object)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('foods:list-food')

        return render(request, 'category_form.html', {'form': form})


class DeleteCategoryView(View):
    @staff_or_superuser_required
    def get(self, request, pk):
        try:
            category_object = Category.objects.get(pk=pk)
            category_object.delete()
            messages.success(request, 'Category deleted successfully!')
            return redirect('foods:list-food')
        except Category.DoesNotExist:
            messages.error(request, 'Category does not exist!')
            return redirect('foods:list-food')



class DeleteFoodView(View):
    @staff_or_superuser_required
    def get(self, request, pk):
        try:
            food_object = Food.objects.get(pk=pk)
            food_object.delete()
            messages.success(request, 'Food deleted successfully!')
            return redirect('foods:list-food')
        except Food.DoesNotExist:
            messages.error(request, 'Food does not exist!')
            return redirect('foods:list-food')

