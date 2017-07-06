from django.contrib import admin

# Register your models here.

from .models import (
    Magazine,
    MagazineDay,
    Guide,
    DetailGuide,
    Asignation,
    DetailAsignation
)

admin.site.register(Magazine)
admin.site.register(MagazineDay)
admin.site.register(Guide)
admin.site.register(DetailGuide)
admin.site.register(Asignation)
admin.site.register(DetailAsignation)
