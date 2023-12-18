from django.contrib import admin
from .models import FoodTagModel
# Register your models here.
@admin.register(FoodTagModel)
class FoodTagAdmin(admin.ModelAdmin):
    pass
