from django.contrib import admin

from .models import Store, Menu, Category

admin.site.register(Store)
admin.site.register(Menu)
admin.site.register(Category)