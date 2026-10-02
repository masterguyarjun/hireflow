from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom User model with account type selection
    """
    ACCOUNT_TYPE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
        ('admin', 'Administrator'),
    ]

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default='job_seeker'
    )

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        help_text="Contact phone number"
    )

    date_of_birth = models.DateField(null=True, blank=True)

    # Override related names to avoid clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='hireflow_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='hireflow_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.get_account_type_display()})"

    @property
    def is_job_seeker(self):
        return self.account_type == 'job_seeker'

    @property
    def is_employer(self):
        return self.account_type == 'employer'

    @property
    def is_admin(self):
        return self.account_type == 'admin'


class JobSeekerProfile(models.Model):
    """
    Profile model for job seekers
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='job_seeker_profile')
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    professional_headline = models.CharField(max_length=200, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    skills = models.TextField(
        help_text="Comma-separated skills (e.g., Python, Django, JavaScript)",
        blank=True
    )
    years_of_experience = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True, help_text="Educational background")
    current_job_title = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"

    def get_skills_list(self):
        """Return skills as a list"""
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []


class EmployerProfile(models.Model):
    """
    Profile model for employers/companies
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=200)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    company_description = models.TextField(max_length=500, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    company_website = models.URLField(blank=True)
    company_location = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(
        max_length=20,
        choices=[
            ('1-10', '1-10 employees'),
            ('11-50', '11-50 employees'),
            ('51-200', '51-200 employees'),
            ('201-500', '201-500 employees'),
            ('501-1000', '501-1000 employees'),
            ('1000+', '1000+ employees'),
        ],
        blank=True
    )
    contact_email = models.EmailField()
    linkedin_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name