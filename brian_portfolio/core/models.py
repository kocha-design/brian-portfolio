from django.db import models
from django.core.exceptions import ValidationError


# ==========================================
# 1. MODELS ZA ASILI
# ==========================================

class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, help_text="e.g., Backend, Frontend, Database, Networking")
    icon = models.CharField(max_length=50, blank=True, default="fa-code", help_text="Font Awesome icon class, e.g., fa-python")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Skills"

    def __str__(self):
        return f"{self.name} ({self.category})"


class Company(models.Model):
    name = models.CharField(max_length=100)
    founded_date = models.DateField()
    description = models.TextField()
    logo = models.ImageField(upload_to='companies/logos/', blank=True, null=True)
    website_url = models.URLField(blank=True, help_text="Official website (optional)")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'founded_date']

    def __str__(self):
        return self.name


class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, default="fa-check-circle", help_text="Font Awesome icon class")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['company', 'order']

    def __str__(self):
        return f"{self.company.name} - {self.title}"


class Project(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    technologies = models.CharField(
        max_length=200,
        help_text="Comma separated, e.g., Python, Django, React"
    )
    link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text="Onyesha kwenye featured section?")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-is_featured', 'order']

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.CharField(max_length=300, blank=True, help_text="Muhtasari mfupi wa article")
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True, default="Portfolio Contact")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


# ==========================================
# 2. MODELS MPYA ZA CMS (Controlled from Admin)
# ==========================================

class SiteSettings(models.Model):
    """
    Model hii inashikilia data zote za jumla za website.
    Inapaswa kuwa na record 1 tu (singleton).
    """

    # ---------- HERO SECTION ----------
    hero_greeting = models.CharField(
        max_length=50,
        default="Hello, I am",
        help_text="Maneno ya kusalimia (greeting)"
    )
    hero_name = models.CharField(
        max_length=100,
        default="Brian Gasto Mrema",
        help_text="Jina lako kamili"
    )
    hero_subtitle = models.CharField(
        max_length=150,
        default="Software Developer | Founder | Technical Director",
        help_text="Cheo chako"
    )
    hero_description = models.TextField(
        default="Passionate software developer specializing in web development, business systems, and digital solutions. Experienced in building scalable web applications, management systems, and modern business websites."
    )
    cv_file = models.FileField(
        upload_to='cv/',
        blank=True,
        null=True,
        help_text="Upload your CV here (PDF format recommended)"
    )

    # ---------- ABOUT SECTION ----------
    about_paragraph_1 = models.TextField(
        verbose_name="About Paragraph 1",
        default="I am a dedicated Software Developer with almost 2 years of experience, holding a Diploma in Computer Science. My journey is driven by a passion for creating robust, scalable, and user-centric digital solutions."
    )
    about_paragraph_2 = models.TextField(
        verbose_name="About Paragraph 2",
        blank=True,
        default="Beyond coding, I am the Founder and Technical Director of two emerging tech companies, where I lead the vision of delivering top-tier Web Development, Systems Development, Networking, and IT Consultancy services to businesses in Tanzania and beyond."
    )

    # ---------- CONTACT & SOCIALS ----------
    contact_email = models.EmailField(default="mremagastobrian@gmail.com")
    contact_phone = models.CharField(max_length=20, default="0613950508")
    contact_location = models.CharField(max_length=100, default="Mbeya, Tanzania")
    linkedin_url = models.URLField(blank=True, default="https://www.linkedin.com/in/briangasto")
    github_url = models.URLField(blank=True, default="https://github.com/kocha-design")
    twitter_url = models.URLField(blank=True, help_text="Twitter/X profile URL (optional)")
    facebook_url = models.URLField(blank=True, help_text="Facebook profile URL (optional)")

    # ---------- FOOTER SECTION ----------
    footer_credit = models.CharField(
        max_length=200,
        default="Designed & Built by Brian Gasto Mrema",
        help_text="Text ya juu ya footer (Designed by...)"
    )
    footer_copyright = models.CharField(
        max_length=200,
        default="© 2026 Random Tech Solution & Obrigado Solutions. All rights reserved.",
        help_text="Text ya chini ya footer (Copyright...)"
    )
    footer_show_social = models.BooleanField(
        default=True,
        help_text="Onyesha social media icons kwenye footer?"
    )
    footer_extra_text = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Maandishi ya ziada kwenye footer (optional)"
    )

    class Meta:
        verbose_name = "Website Setting"
        verbose_name_plural = "Website Settings"

    def __str__(self):
        return "Global Website Settings"

    def save(self, *args, **kwargs):
        # Kuzuia kuunda settings zaidi ya moja (singleton)
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError('There can be only one SiteSettings instance. Please edit the existing one.')
        return super(SiteSettings, self).save(*args, **kwargs)


class Stat(models.Model):
    """Namba za kwenye About Section (e.g., 2+ Years Exp)"""
    value = models.CharField(max_length=20, help_text="e.g., 2+, 100%, 10+")
    label = models.CharField(max_length=50, help_text="e.g., Years Exp., Companies")
    order = models.IntegerField(default=0, help_text="Lower number appears first")

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Stats"

    def __str__(self):
        return f"{self.value} - {self.label}"


class Experience(models.Model):
    """Timeline ya kazi na elimu"""
    title = models.CharField(max_length=150)
    period = models.CharField(max_length=50, help_text="e.g., 2024 - Present")
    description = models.TextField()
    is_current = models.BooleanField(default=False, help_text="Check if this is your current role")
    order = models.IntegerField(default=0, help_text="Lower number appears first")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """Maoni ya wateja au wafanyakazi wenzako"""
    client_name = models.CharField(max_length=100)
    client_role = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.client_name