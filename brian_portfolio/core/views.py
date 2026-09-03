from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Skill, Company, Project, BlogPost, SiteSettings, Stat, Experience, Testimonial, ContactMessage

# --- View yako ya awali ya Home ---
def portfolio_home(request):
    settings = SiteSettings.objects.first()
    skills = Skill.objects.all()
    companies = Company.objects.prefetch_related('services').all()
    projects = Project.objects.all()[:8]
    blog_posts = BlogPost.objects.order_by('-created_at')[:3]
    stats = Stat.objects.all()
    experiences = Experience.objects.all()
    testimonials = Testimonial.objects.all()
    
    for project in projects:
        if project.technologies:
            project.tech_list = [tech.strip() for tech in project.technologies.split(',')]
        else:
            project.tech_list = []
    
    context = {
        'settings': settings,
        'skills': skills,
        'companies': companies,
        'projects': projects,
        'blog_posts': blog_posts,
        'stats': stats,
        'experiences': experiences,
        'testimonials': testimonials,
    }
    return render(request, 'core/index.html', context)


# --- 🔥 ONGEZA VIEW HII MPYA YA CONTACT SUBMIT ---
def contact_submit(request):
    if request.method == 'POST':
        # Chukua data kutoka kwenye form
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', 'Portfolio Contact Message')
        message = request.POST.get('message')
        
        # Hifadhi kwenye database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Onyesha ujumbe wa mafanikio (optional)
        messages.success(request, "Thank You For Contacting Me! I will be back to you soon 👏👏.")
        
        # 🔥 REKEBISHO KUU HAPA: 
        # reverse('home') inarudisha '/' kisha tunaongeza '#contact' mwishoni
        return HttpResponseRedirect(reverse('home') + '#contact')
        
    # Kama si POST request, rudisha home tu
    return redirect('home')