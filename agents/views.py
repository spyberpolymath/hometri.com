from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Agent, AgentContact, AgentPropertyContact
from django.core.paginator import Paginator
from hometri.models import Listening

def agent_list(request):
    ordered_roles = [
        "Real Estate Agent Manager",
        "Real Estate Agent Team Leader",
        "Real Estate Agent Admin (Ops Administrator)",
        "Real Estate Agent"
    ]
    all_agents = Agent.objects.all()
    agents_by_role = {role: [] for role in ordered_roles}
    real_estate_agents = []
    for agent in all_agents:
        if agent.title in ordered_roles:
            agents_by_role[agent.title].append(agent)
        else:
            real_estate_agents.append(agent)
    return render(request, 'agents/agents_list.html', {
        'ordered_roles': ordered_roles,
        'agents_by_role': agents_by_role,
        'real_estate_agents': real_estate_agents
    })

def agent_detail(request, agent_id):
    agent = get_object_or_404(Agent, pk=agent_id)
    # Get all properties listed by this agent
    agent_properties = Listening.objects.filter(agent=agent)
      # Split work experience into points
    if agent.work_experience:
        work_experience_points = [point.strip() for point in agent.work_experience.split('|') if point.strip()]
    else:
        work_experience_points = []
        
    return render(request, 'agents/agent_detail.html', {
        'agent': agent, 
        'agent_properties': agent_properties,
        'work_experience_points': work_experience_points
    })

def agent_property_contact(request):
    if request.method == 'POST':
        agent_name = request.POST['agentname']
        property_title = request.POST['property_title']
        user_name = request.POST['name']
        user_email = request.POST['email']
        user_phone = request.POST['number']
        user_subject = request.POST['textarea']
        agent_id = request.POST.get('agent_id')
        property_slug = request.POST.get('property_slug')
        
        contact = AgentPropertyContact.objects.create(
            agentname=agent_name,
            property_title=property_title,
            user_name=user_name,
            user_email=user_email,
            user_phone=user_phone,
            user_subject=user_subject
        )
        
        messages.success(request, "Thank you! The agent will contact you about this property soon.")
        # Redirect back to the property detail page
        return redirect('property_detail', slug=property_slug)

def agentcontact(request):
    if request.method == 'POST':
        agent_name = request.POST['agentname']
        user_name = request.POST['name']
        user_email = request.POST['email']
        user_phone = request.POST.get('phone', '')  # Making phone optional
        user_subject = request.POST['textarea']
        agent_id = request.POST.get('agent_id')
        
        contact = AgentContact.objects.create(
            agentname=agent_name,
            user_name=user_name,
            user_email=user_email,
            user_phone=user_phone,
            user_subject=user_subject
        )
        messages.success(request, "Thank you! Your message has been sent to the agent.")

        # Redirect back to agent detail page
        return redirect('agent_detail', agent_id=agent_id)
