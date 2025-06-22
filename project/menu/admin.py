from django.contrib import admin

from .models import Store, Menu, Category , Review , VisitLog , Like

admin.site.register(Store)
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(VisitLog)
admin.site.register(Like)