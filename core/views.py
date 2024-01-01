from django.shortcuts import render
from django.views import View
from utils import Reporting, staff_or_superuser_required
from decimal import Decimal


# Create your views here.
class HomeView(View):
    template_name = 'Core_HomeTemplate.html'

    def get(self, request):
        try:
            context = {'name': request.user.phone_number}
        except Exception:
            context = {'name': None}
        return render(request, self.template_name, context)


class DashboardView(View):
    template_name = 'Core_DashboardTemplate.html'

    @staff_or_superuser_required
    def get(self, request):
        selected_range = request.GET.get('range', 'month')  # Default to 'month' if not specified

        if selected_range == 'year':
            days = 365
        elif selected_range == 'week':
            days = 7
        elif selected_range == 'day':
            days = 1
        elif selected_range == 'month':
            days = 30
        elif selected_range == 'total':
            days = 99999

        r = Reporting(days)
        total_sales: Decimal = r.total_sales()
        percentage_difference = r.get_percentage_difference()

        context = {
            'total_sales': total_sales,
            'percentage_difference': -percentage_difference,
            'favorite_food': r.favorite_foods(),
            'favorite_table': r.favorite_tables(),
            'peak_hour': r.peak_hours(),
        }

        return render(request, self.template_name, context=context)
