from django.contrib import admin
from .models import Tag,TaggedItem

# Register your models here.

#todo : fix admin tag modifying

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['label']

@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    search_fields = ['label']
