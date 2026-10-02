from django.db import models
from user_accounts.models import EmployerProfile


class Company(models.Model):
    """
    Company model for showcasing employers
    """
    employer_profile = models.OneToOneField(EmployerProfile, on_delete=models.CASCADE, related_name='company')
    founded_year = models.PositiveIntegerField(null=True, blank=True)
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
    headquarters = models.CharField(max_length=100, blank=True)
    specialties = models.TextField(
        help_text="Comma-separated specialties (e.g., Software Development, AI, Cloud Computing)",
        blank=True
    )
    culture_description = models.TextField(
        help_text="Description of company culture and values",
        blank=True
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Verified companies have been authenticated"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employer_profile.company_name

    def get_specialties_list(self):
        """Return specialties as a list"""
        if self.specialties:
            return [spec.strip() for spec in self.specialties.split(',')]
        return []