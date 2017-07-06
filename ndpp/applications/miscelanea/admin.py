from django.contrib import admin

# Register your models here.

from .models import Provider, Vendor

admin.site.register(Provider)
admin.site.register(Vendor)
