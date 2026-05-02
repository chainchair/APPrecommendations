from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Interest, CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'interests')
    search_fields = ('username', 'email')
    filter_horizontal = ('interests',)
    
    def get_queryset(self, request):
        # Opcional: por defecto muestra solo usuarios normales
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_staff=False)
        return qs


admin.site.register(Interest)
admin.site.register(CustomUser, CustomUserAdmin)
