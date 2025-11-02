from django.contrib import admin
from django.http import HttpResponse

from .models import Listening, Contact, Quickcontact, Newsletter
from .locations_data import locations
from django import forms


@admin.register(Listening)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'agent', 'title', 'slug', 'image', 'image2', 'image3', 'description', 'location', 'price',
        'bedrooms', 'bathrooms', 'area', 'kitchen', 'garage', 'created', 'available', 'status',
        'marketing_priority'
    )
    list_filter = ('status', 'available', 'agent', 'created', 'marketing_priority')
    search_fields = ('title', 'location', 'description')
    actions = ['mark_as_unavailable']
    ordering = ('-created',)

    def has_add_permission(self, request):
        # Allow all authenticated users to add listings
        return request.user.is_authenticated

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        # Check all possible roles
        for app_name in ['agent_role', 'team_role', 'crm_role', 'marketing_role']:
            try:
                role = getattr(request.user, app_name, None)
                if role and role.role in ['admin', 'manager']:
                    return True
            except:
                continue
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        # Only admins can delete
        for app_name in ['agent_role', 'team_role', 'crm_role', 'marketing_role']:
            try:
                role = getattr(request.user, app_name, None)
                if role and role.role == 'admin':
                    return True
            except:
                continue
        return False

    def mark_as_unavailable(self, request, queryset):
        queryset.update(available=False)
    mark_as_unavailable.short_description = "Mark selected listings as unavailable"

    # export_as_csv and export_as_excel removed


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    actions = []

    # export_as_csv and export_as_excel removed


@admin.register(Quickcontact)
class QuickContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')
    actions = []

    # export_as_csv and export_as_excel removed


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'whatsapp_updates',
                    'is_active', 'date_subscribed')
    list_filter = ('whatsapp_updates', 'is_active', 'date_subscribed')
    search_fields = ('name', 'email', 'phone')
    ordering = ('-date_subscribed',)
    actions = ['activate_subscriptions', 'deactivate_subscriptions']

    def activate_subscriptions(self, request, queryset):
        queryset.update(is_active=True)
    activate_subscriptions.short_description = "Activate selected subscriptions"

    def deactivate_subscriptions(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"

    # export_as_csv and export_as_excel removed
