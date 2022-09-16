from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Navire)
class NavireAdmin(admin.ModelAdmin):
    list_display = ["matricule"]


@admin.register(Mareyeur)
class MareyeurAdmin(admin.ModelAdmin):
    list_display = ["code_national"]


@admin.register(CinMareyeur, RcStatutMareyeur, ActeCessionMareyeur, CarteAutorisationMareyeur, DiversMareyeur,
                ActeNationaliteNavire, ArmateurRcNavire, ActeCessionNavire, DiversNavire)
class MareyeurDocumentAdmin(admin.ModelAdmin):
    list_display = ["id", "file", "date_creation", "date_modification", "client"]
    list_filter = ["client"]
