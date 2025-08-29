from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form        = CustomUserCreationForm
    form            = CustomUserChangeForm
    model           = CustomUser

    list_display    = [
        'email', 'first_name', 'last_name', 'role',
    ]

    add_fieldsets = UserAdmin.add_fieldsets + (('USER ROLE', {'fields': ('role',)}),)

    fieldsets     = UserAdmin.fieldsets + (('USER ROLE', {'fields': ('role',)}),)


admin.site.register(CustomUser, CustomUserAdmin)