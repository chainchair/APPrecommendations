from django.contrib import admin
from .models import Place, Category

admin.site.register(Category)

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    exclude = ('slug',)