from django.contrib import admin
from .models import Opportunity, Application

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ['company', 'role', 'type', 'domain', 'deadline', 'posted_by']
    list_filter  = ['type', 'domain']
    search_fields = ['company', 'role', 'posted_by__full_name']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'opportunity', 'status', 'applied_at']
    list_filter  = ['status']
    search_fields = ['student__full_name', 'opportunity__company']