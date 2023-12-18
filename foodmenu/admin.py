from django.contrib import admin
from .models import Food, Category
# Register your models here.
@admin.register(Food)
class FoodTagAdmin(admin.ModelAdmin):
    pass