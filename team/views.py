from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
 
import csv
import json
from .models import Team, TeamContactMessage
from agents.models import Agent

def team(request):
    teams = Team.objects.order_by('created_at').filter(is_published=True)
    agents = Agent.objects.order_by('-hire_date')
    
    # Define team structure with categories
    team_structure = {
        '🧭 Strategic & Management Group': [
            'Founder & CEO',
            'Accounting and Financial Manager',
            'HR Manager',
            'Team Admin (CRM Administrator)',
            'Team Admin',
            'CRM Administrator'
        ],
        '💻 IT & Digital Infrastructure Team': [
            'IT Support Manager',
            'IT Support Team Leader',
            'IT Support Engineer (Developer, Data Analyst, Infrastructure)',
            'IT Support Engineer',
            'Developer',
            'Data Analyst',
            'Infrastructure'
        ],
        '☎️ Customer Support & Relations': [
            'Customer Support Manager',
            'Customer Support Team Leader',
            'Customer Support'
        ],
        '🏠 Real Estate Agents': [
            'Real Estate Agent Manager',
            'Real Estate Agent Team Leader',
            'Real Estate Agent Admin (Ops Administrator)',
            'Real Estate Agent Admin',
            'Ops Administrator',
            'Real Estate Agent'
        ],
        '💰 Sales Team': [
            'Sales Manager',
            'Sales Team Leader',
            'Sales Executive',
            'Sales'
        ],
        '📣 Marketing Team': [
            'Marketing Team Group',
            'Marketing Manager',
            'Marketing Team Leader',
            'Marketing Executive',
            'Marketing'
        ]
    }
    
    import re
    def clean_title(title):
        # Remove parenthesis and their contents, then strip and lowercase
        return re.sub(r'\s*\([^)]*\)', '', title).strip().lower()


    organized_teams = {}
    for category, roles in team_structure.items():
        organized_teams[category] = []
        added_ids = set()
        for role in roles:
            role_key = clean_title(role)
            matching_members = [tm for tm in teams if tm.id not in added_ids and clean_title(tm.title) == role_key]
            for tm in matching_members:
                organized_teams[category].append(tm)
                added_ids.add(tm.id)
    
    context = {
        'teams': teams,
        'agents': agents,
        'organized_teams': organized_teams,
        'team_structure': team_structure
    }
    return render(request, 'team/team.html', context)

def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    work_experience = team.work_experience_as_list()
    
    context = {
        'team': team,
        'work_experience': work_experience
    }
    return render(request, 'team/team_detail.html', context)

def team_contact(request, team_id):
    if request.method == 'POST':
        team = get_object_or_404(Team, pk=team_id)
        
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        
        # Validate inputs
        if not all([name, email, phone, message]):
            # Return to team detail page with error message
            messages.error(request, 'All fields are required.')
            return redirect('team:team_detail', team_id=team_id)
        
        # Create contact message
        contact = TeamContactMessage(
            team=team,
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        contact.save()
        
        # Add success message and redirect to team detail page
        messages.success(request, 'Your message has been sent successfully. We\'ll get back to you soon.')
        return redirect('team:team_detail', team_id=team_id)
    
    # If not POST, redirect to team detail page
    return redirect('team:team_detail', team_id=team_id)

def sync_with_apps(request):
    # Sync logic here (removed TeamRole checks)
    
    try:
        data = json.loads(request.body)
        direction = data.get('direction', 'to')  # 'to' or 'from'
        target_app = data.get('app', 'all')
        synced_count = 0
        if direction == 'to':
            pass
        else:
            pass
        return JsonResponse({
            'success': True,
            'synced_count': synced_count,
            'message': f'Successfully synced {synced_count} team members'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

## export_team_data removed

def check_user_role(request):
    """API endpoint to check the current user's team role. Placeholder implementation."""
    if request.user.is_authenticated:
        # Placeholder: return a dummy role. Replace with actual logic as needed.
        return JsonResponse({'role': 'member', 'user': request.user.username})
    else:
        return JsonResponse({'role': 'anonymous', 'user': None})
