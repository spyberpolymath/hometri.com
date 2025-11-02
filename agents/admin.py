from django.contrib import admin
from django.http import HttpResponse
from .models import Agent, AgentContact, AgentPropertyContact, WorkNote

class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email', 'phone')
    search_fields = ('name', 'email', 'title')
    # actions removed: export_as_csv, export_as_excel
    fieldsets = (
        (None, {
            'fields': ('name', 'title', 'photo', 'email', 'phone', 'hire_date')
        }),
        ('Social Media', {
            'fields': ('whatsapp', 'instagram', 'linkedin')
        }),
        ('Profile Content', {
            'fields': ('description', 'work_experience'),
            'description': 'For work experience, enter each point/achievement separated by the | (pipe) character. Each point will be displayed as a bullet point on the frontend.'
        })
    )
    
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
      
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role in ['admin', 'manager']:
                return qs
            elif agent_role.role == 'agent':
                # Employees can only see their own profile
                return qs.filter(email=request.user.email)
        except AgentRole.DoesNotExist:
            return qs.none()
        return qs
    
    # export_as_csv and export_as_excel removed

class AgentContactAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'agentname', 'user_email', 'contact_date')
    list_filter = ('agentname', 'contact_date')
    search_fields = ('user_name', 'user_email', 'agentname')
    ordering = ('-contact_date',)
    # actions removed: export_as_csv, export_as_excel
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role in ['admin', 'manager']:
                return True
            # Employees can only view contacts for themselves
            elif agent_role.role == 'agent' and obj:
                return obj.agentname == request.user.first_name + ' ' + request.user.last_name
            return False
        except AgentRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            return agent_role.role in ['admin', 'manager']
        except AgentRole.DoesNotExist:
            return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role in ['admin', 'manager']:
                return qs
            elif agent_role.role == 'agent':
                # Employees can only see contacts for themselves
                agent_name = request.user.first_name + ' ' + request.user.last_name
                return qs.filter(agentname=agent_name)
        except AgentRole.DoesNotExist:
            return qs.none()
        return qs
    
    # export_as_csv and export_as_excel removed

class AgentPropertyContactAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'agentname', 'property_title', 'user_email', 'contact_date')
    list_filter = ('agentname', 'contact_date', 'property_title')
    search_fields = ('user_name', 'user_email', 'agentname', 'property_title')
    ordering = ('-contact_date',)
    # actions removed: export_as_csv, export_as_excel
    
    def has_add_permission(self, request):
        return True
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role in ['admin', 'manager']:
                return True
            # Employees can only view contacts for themselves
            elif agent_role.role == 'agent' and obj:
                return obj.agentname == request.user.first_name + ' ' + request.user.last_name
            return False
        except AgentRole.DoesNotExist:
            return False
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            return agent_role.role in ['admin', 'manager']
        except AgentRole.DoesNotExist:
            return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role in ['admin', 'manager']:
                return qs
            elif agent_role.role == 'agent':
                # Employees can only see contacts for themselves
                agent_name = request.user.first_name + ' ' + request.user.last_name
                return qs.filter(agentname=agent_name)
        except AgentRole.DoesNotExist:
            return qs.none()
        return qs
    
    # export_as_csv and export_as_excel removed

class WorkNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date_created', 'date_updated')
    list_filter = ('date_created', 'date_updated', 'user')
    search_fields = ('title', 'description', 'user__username')
    ordering = ('-date_created',)
    # actions removed: export_as_csv
    
    fieldsets = (
        ('Note Information', {
            'fields': ('title', 'description')
        }),
        ('Related Records', {
            'fields': ('related_customer_id', 'related_property_id', 'related_lead_id'),
            'description': 'Optional: Link this note to specific records'
        }),
    )
    
    def has_add_permission(self, request):
        # All logged in users can add work notes
        return request.user.is_authenticated
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role in ['admin', 'manager']:
                return True
            elif obj:
                # Users can only edit their own notes
                return obj.user == request.user
            return False
        except AgentRole.DoesNotExist:
            # If no role, users can still edit their own notes
            return obj and obj.user == request.user
    
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role == 'admin':
                return True
            elif obj:
                # Users can delete their own notes
                return obj.user == request.user
            return False
        except AgentRole.DoesNotExist:
            # If no role, users can still delete their own notes
            return obj and obj.user == request.user
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        try:
            agent_role = AgentRole.objects.get(user=request.user)
            if agent_role.role in ['admin', 'manager']:
                return qs
            else:
                # Users can only see their own notes
                return qs.filter(user=request.user)
        except AgentRole.DoesNotExist:
            # If no role, users can still see their own notes
            return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new note
            obj.user = request.user
        super().save_model(request, obj, form, change)
    
    # export_as_csv removed

# Register models
admin.site.register(Agent, AgentAdmin)
admin.site.register(AgentContact, AgentContactAdmin)
admin.site.register(AgentPropertyContact, AgentPropertyContactAdmin)
admin.site.register(WorkNote, WorkNoteAdmin)