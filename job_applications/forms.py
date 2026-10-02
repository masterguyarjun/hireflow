from django import forms
from .models import Application
import os


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Tell us why you are interested in this position and what makes you a good fit...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resume'].widget.attrs.update({
            'class': 'form-control',
            'accept': '.pdf,.doc,.docx'
        })
        self.fields['resume'].help_text = "Upload your resume (PDF, DOC, or DOCX format, max 5MB)"

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Check file size (5MB limit)
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 5MB.")

            # Check file extension
            ext = os.path.splitext(resume.name)[1].lower()
            allowed_extensions = ['.pdf', '.doc', '.docx']
            if ext not in allowed_extensions:
                raise forms.ValidationError("Unsupported file format. Please upload PDF, DOC, or DOCX files only.")

        return resume