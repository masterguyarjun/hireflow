from django.db import models
from django.conf import settings
from job_listings.models import Job
from user_accounts.models import JobSeekerProfile


class Application(models.Model):
    """
    Model for job applications
    """
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    resume = models.FileField(upload_to='application_resumes/', help_text="PDF, DOC, or DOCX format")
    cover_letter = models.TextField(
        help_text="Why you're interested in this position and what makes you a good fit",
        blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    employer_notes = models.TextField(blank=True, help_text="Internal notes from employer")

    class Meta:
        ordering = ['-applied_at']
        # Prevent duplicate applications
        unique_together = ('job', 'applicant')
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['applied_at']),
            models.Index(fields=['job', 'status']),
        ]

    def __str__(self):
        return f"{self.applicant.get_full_name()} - {self.job.title}"

    def save(self, *args, **kwargs):
        # Validate file extension
        if self.resume:
            import os
            ext = os.path.splitext(self.resume.name)[1].lower()
            allowed_extensions = ['.pdf', '.doc', '.docx']
            if ext not in allowed_extensions:
                raise ValueError("Unsupported file format. Please upload PDF, DOC, or DOCX files only.")
        super().save(*args, **kwargs)

    @property
    def days_since_applied(self):
        from django.utils import timezone
        return (timezone.now() - self.applied_at).days