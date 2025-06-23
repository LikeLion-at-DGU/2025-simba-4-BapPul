from django.contrib import admin
from .models import RiceMap, RiceGrain, Riceball

@admin.register(RiceMap)
class RiceMapAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('owner__nickname',)

@admin.register(RiceGrain)
class RiceGrainAdmin(admin.ModelAdmin):
    list_display = ('id', 'rice_map', 'date', 'review_id', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('rice_map__owner__nickname',)

@admin.register(Riceball)
class RiceballAdmin(admin.ModelAdmin):
    list_display = ('id', 'rice_map', 'created_at', 'reward_given')
    list_filter = ('created_at', 'reward_given')
    search_fields = ('rice_map__owner__nickname',)
