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
        r = Reporting()
        total_sales = r.total_sales()
        context = {'total_sales' : total_sales}
        return render(request, self.template_name, context=context)
