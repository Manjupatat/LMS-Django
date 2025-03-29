# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_student', 'is_instructor',]
    fieldsets = UserAdmin.fieldsets + (
        ('User Role', {'fields': ('is_student', 'is_instructor')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
