from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import path
from django.utils.html import format_html
from .models import Team, TeamContactMessage

class TeamAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.photo and hasattr(object.photo, 'url'):
            return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.photo.url))
        return format_html('<div style="width: 40px; height: 40px; background-color: #ccc; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px;">No Photo</div>')

    thumbnail.short_description = 'Photo'
    
    list_display = ('id', 'thumbnail', 'name', 'title', 'role', 'email', 'phone', 'is_published')
    list_display_links = ('id', 'thumbnail', 'name')
    list_filter = ('is_published', 'role', 'hire_date')
    list_editable = ('is_published',)
    search_fields = ('name', 'title', 'email', 'role')
    list_per_page = 25
    actions = ['sync_to_other_apps']
    
    readonly_fields = ['work_experience_as_html']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'photo', 'title', 'description')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'whatsapp', 'instagram', 'linkedin')
        }),
        ('Work Details', {
            'fields': ('role', 'hire_date', 'work_experience', 'work_experience_as_html')
        }),
    )
    
    # Removed get_urls and changelist_view for import/export actions
    
    list_display = ('id', 'thumbnail', 'name', 'title', 'role', 'email', 'phone', 'is_published')
    list_display_links = ('id', 'thumbnail', 'name')
    list_filter = ('is_published', 'role', 'hire_date')
    list_editable = ('is_published',)
    search_fields = ('name', 'title', 'email', 'role')
    list_per_page = 25
    actions = ['sync_to_other_apps']
    
    readonly_fields = ['work_experience_as_html']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'photo', 'title', 'description')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'whatsapp', 'instagram', 'linkedin')
        }),
        ('Work Details', {
            'fields': ('role', 'hire_date', 'work_experience', 'work_experience_as_html')
        }),
        ('System Access', {
            'fields': ('is_published',),
            'description': 'System access control'
        }),
    )
    
    # Removed get_urls and changelist_view for import/export actions
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        try:
            user_role = TeamRole.objects.get(user=request.user)
            return user_role.role in ['admin', 'manager']
        except TeamRole.DoesNotExist:
            return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            user_role = TeamRole.objects.get(user=request.user)
            return user_role.role in ['admin', 'manager']
        except TeamRole.DoesNotExist:
            return False
    
    
    def sync_to_other_apps(self, request, queryset):
        """Sync selected team members to other apps"""
        synced_count = 0
        for team in queryset:
            if hasattr(team, 'sync_with_other_apps') and team.role in ['admin', 'manager']:
                team.sync_with_other_apps()
                synced_count += 1
        
        self.message_user(request, f'Successfully synced {synced_count} team members to other apps.')
    sync_to_other_apps.short_description = "Sync selected members to other apps"
    

class TeamContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'email', 'phone', 'created_at', 'is_read')
    list_filter = ('team', 'created_at', 'is_read')
    search_fields = ('name', 'email', 'phone', 'team__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    actions = ['mark_as_read', 'mark_as_unread']
        
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"
    

# Register models
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamContactMessage, TeamContactMessageAdmin)
