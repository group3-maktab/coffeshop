from django.contrib import admin
from .models import CustomUser
# Register your models here.
from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission,User
from .models import CustomUser


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    search_fields = ['codename']
    pass


class PermissionInline(admin.TabularInline):
    autocomplete_fields = ['permission']
    model = CustomUser.user_permissions.through
    extra = 1


class GroupInline(admin.TabularInline):
    autocomplete_fields = ['group']
    model = CustomUser.groups.through
    extra = 0


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    admin.site.unregister(User)
    list_display = ('phone_number', 'email','is_active', 'is_staff', 'last_login')
    readonly_fields = ('last_login', 'phone_number','email')

    fieldsets = (
        (None, {'fields': ['phone_number', 'email']}),
        ('Permissions', {'fields': ['is_active', 'is_staff', 'groups', 'user_permissions']}),
        ('Last_login', {'fields': ['last_login',]}),
    )

    add_fieldsets = (
        (None, {
            'classes': ['wide'],
            'fields': ['phone_number','email',],
        }),
        # ('Permitions',{'fields': ['is_active', 'is_staff']})
    )

    search_fields = ('phone_number','email')
    ordering = ('phone_number','email')
    filter_horizontal = ('groups', 'user_permissions')

    inlines = [PermissionInline, GroupInline]
