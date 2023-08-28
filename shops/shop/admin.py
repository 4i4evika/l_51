from django.contrib import admin
from .models import *


class ShopAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Shop)