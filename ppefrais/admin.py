from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# class CustomUserAdmin(UserAdmin):
#     form = CustomUserChangeForm
#     add_form = CustomUserCreationForm


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('statut', 'adresse', 'code_postal', 'date_embauche')


admin.site.register(CustomUser, CustomUserAdmin)
