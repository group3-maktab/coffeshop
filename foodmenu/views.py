from django.shortcuts import render
from django.views import View
from .utils import json_menu_generator
from .models import Food, Category


class ListFoodView(View):
    template_name = 'Food_ListTemplate.html'
    def get(self, request):

        menu_data = json_menu_generator()
        return render(request, self.template_name, {'menu_data': menu_data})
