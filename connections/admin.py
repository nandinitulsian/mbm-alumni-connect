from django.contrib import admin
from .models import Connection

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display  = ['student', 'alumni', 'status', 'created_at']
    list_filter   = ['status']
    search_fields = ['student__full_name', 'alumni__full_name']