from django.shortcuts import render
from django.views import View
from utils import Reporting
# Create your views here.
class HomeView(View):
    template_name = 'Core_HomeTemplate.html'
    def get(self,request):
        return render(request, self.template_name)

class DashboardView(View):
    template_name = 'Core_DashboardTemplate.html'
    def get(self,request):
        r = Reporting(30)
        total_sales = r.total_sales()
        favorite_table = []
        favorite_food = []
        for table in r.favorite_tables():
            favorite_table.append(f"Table #{table.number} - Seats: {table.used_seats}")
        for food in r.favorite_foods():
            favorite_food.append(f"{food} | {food.used_foods}")
        context = {'total_sales' : total_sales,
                   'favorite_food' : favorite_food ,
                   'favorite_table' : favorite_table}
        return render(request, self.template_name, context=context)
