from django.contrib import admin
from .models import (
    Skill, Company, Service, Project, BlogPost, ContactMessage,
    SiteSettings, Stat, Experience, Testimonial
)


# ==========================================
# 1. ADMIN YA MODELS MPYA (CMS)
# ==========================================

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admin ya Website Settings (Singleton - record 1 tu)"""

    def has_add_permission(self, request):
        # Kuzuia admin kuongeza setting ya pili
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Kuzuia kufuta setting (lazima iwe na moja kila wakati)
        return False

    fieldsets = (
        ('🏠 Hero Section', {
            'fields': ('hero_greeting', 'hero_name', 'hero_subtitle', 'hero_description', 'cv_file'),
            'description': 'Taarifa za sehemu ya juu ya website (Hero banner)',
        }),
        ('👤 About Section', {
            'fields': ('about_paragraph_1', 'about_paragraph_2'),
            'description': 'Bio yako na maelezo mafupi',
        }),
        ('📞 Contact & Socials', {
            'fields': (
                'contact_email', 'contact_phone', 'contact_location',
                'linkedin_url', 'github_url', 'twitter_url', 'facebook_url'
            ),
            'description': 'Njia za kuwasiliana nawe na social media',
        }),
        ('📄 Footer Section', {
            'fields': (
                'footer_credit', 'footer_copyright',
                'footer_show_social', 'footer_extra_text'
            ),
            'description': 'Taarifa za sehemu ya chini ya website (Footer)',
            'classes': ('collapse',),
        }),
    )


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('value', 'label', 'order')
    list_editable = ('order',)
    ordering = ('order',)
    search_fields = ('label',)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'period', 'is_current', 'order')
    list_editable = ('is_current', 'order')
    list_filter = ('is_current',)
    ordering = ('order',)
    search_fields = ('title',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_role', 'created_at')
    ordering = ('-created_at',)
    search_fields = ('client_name', 'message')


# ==========================================
# 2. ADMIN YA MODELS ZA ASILI
# ==========================================

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon', 'order')
    list_editable = ('order', 'category')
    list_filter = ('category',)
    ordering = ('order', 'name')
    search_fields = ('name',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'founded_date', 'order')
    list_editable = ('order',)
    ordering = ('order', 'founded_date')
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'order')
    list_filter = ('company',)
    list_editable = ('order',)
    ordering = ('company', 'order')
    search_fields = ('title', 'description')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'technologies', 'is_featured', 'order')
    list_filter = ('is_featured',)
    list_editable = ('is_featured', 'order')
    ordering = ('-is_featured', 'order')
    search_fields = ('title', 'technologies', 'description')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
    search_fields = ('title', 'content')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    list_editable = ('is_read',)
    ordering = ('-created_at',)
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    search_fields = ('name', 'email', 'message')

    def has_add_permission(self, request):
        # Contact messages zinakuja kutoka form tu, si admin
        return False