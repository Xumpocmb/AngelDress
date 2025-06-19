from django.contrib import admin
from .models import ClientCallBack

@admin.register(ClientCallBack)
class ClientCallBackAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'email')
    ordering = ('-created_at',)
    list_editable = ('status',)
