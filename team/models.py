from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)



# Create your models here.
class Team(models.Model):
    ROLE_CHOICES = [
        ('member', 'Team Member'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
        ('lead', 'Team Lead'),
        ('hr manager', 'HR Manager'),
    ]
    
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    work_experience = models.TextField(
        blank=True,
        help_text="Enter work experience points separated by the '|' character. Each point will be displayed as a separate bullet point on the frontend."
    )
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='member',
        help_text="Role of the team member in organization"
    )
    hire_date = models.DateField(null=True, blank=True)
    # user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, help_text="Link to user account if team member has system access")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def work_experience_as_list(self):
        """Returns work_experience as a list of bullet points"""
        return [exp.strip() for exp in self.work_experience.split('|') if exp.strip()]

    def work_experience_as_html(self):
        """Returns work_experience as HTML bullet list"""
        items = self.work_experience_as_list()
        if not items:
            return "-"
        return format_html("<ul>{}</ul>", format_html("".join(f"<li>{item}</li>" for item in items)))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('team:team_detail', args=[str(self.id)])


class TeamContactMessage(models.Model):
    team = models.ForeignKey(Team, related_name='contact_messages', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} to {self.team.name}"

    class Meta:
        ordering = ['-created_at']

# Reverse sync signals from other apps
def sync_from_agents():
    """Sync data from agents app to team"""    
    try:
        from agents.models import Agent
        
        @receiver(post_save, sender=Agent)
        def agent_post_save(sender, instance, created, **kwargs):
            try:
                team, team_created = Team.objects.get_or_create(
                    email=instance.email,
                    defaults={
                        'name': instance.name,
                        'title': 'Real Estate Agent',
                        'description': instance.description,
                        'photo': instance.photo,
                        'phone': instance.phone,
                        'role': 'manager',
                        # 'user': instance.user,
                        'is_published': True
                    }
                )
                if not team_created:
                    # Update existing team record
                    team.name = instance.name
                    team.description = instance.description
                    team.phone = instance.phone
                    team.role = 'manager'
                    # team.user = instance.user
                    team.is_published = True
                    team.save()
                    
            except Exception as e:
                logger.error(f"Error syncing agent {instance.name} to team: {str(e)}")
                
    except ImportError:
        pass


def sync_from_crm():
    """Sync data from CRM app to team"""
    try:
        from crm.models import CRMUser
        
        @receiver(post_save, sender=CRMUser)
        def crm_user_post_save(sender, instance, created, **kwargs):
            try:
                # TODO: Implement CRM user to team sync logic here
                pass
            except Exception as e:
                logger.error(f"Error syncing CRM user to team: {str(e)}")
                
    except ImportError:
        pass


# Initialize reverse sync
sync_from_agents()
sync_from_crm()

# Add utility function for receiving CRM transfers
def receive_crm_transfer(transfer_data):
    """Receive customer data from CRM and create team lead/contact"""
    try:
        from crm.models import DataTransfer
        
        transfer_id = transfer_data.get('transfer_id')
        customer_data = transfer_data.get('customer_data')
        
        # Create a team contact message or work note based on the transfer
        # This is where the team app would process incoming customer data
        
        # Update transfer status
        if transfer_id:
            transfer = DataTransfer.objects.get(id=transfer_id)
            transfer.status = 'received'
            transfer.save()
            
        return True
        
    except Exception as e:
        logger.error(f"Error receiving CRM transfer: {str(e)}")
        try:
            from crm.models import CRMUser
            pass
        except ImportError:
            pass
