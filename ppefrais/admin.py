from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import Visiteur, FicheFrais, LigneFraisHorsForfait, LigneFraisForfait


class VisiteurChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Visiteur


class CustomUserAdmin(UserAdmin):
    form = VisiteurChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nom', 'prenom', 'adresse', 'code_postal', 'ville', 'date_embauche',)}),
    )


admin.site.register(Visiteur, CustomUserAdmin)
admin.site.register(FicheFrais),
admin.site.register(LigneFraisHorsForfait),
admin.site.register(LigneFraisForfait),
