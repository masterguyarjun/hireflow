from django import forms
from .models import Job, Category, Skill


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['employer', 'slug', 'created_at', 'updated_at', 'published_at', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'responsibilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'benefits': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'application_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'salary_currency': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('USD', 'USD ($)'),
                ('EUR', 'EUR (€)'),
                ('GBP', 'GBP (£)'),
                ('CAD', 'CAD (C$)'),
                ('AUD', 'AUD (A$)'),
                ('INR', 'INR (₹)'),
            ]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make category and skills fields better
        self.fields['category'] = forms.ModelChoiceField(
            queryset=Category.objects.all(),
            empty_label="Select a category",
            widget=forms.Select(attrs={'class': 'form-select'})
        )
        self.fields['skills'] = forms.ModelMultipleChoiceField(
            queryset=Skill.objects.all(),
            required=False,
            widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '8'})
        )
        self.fields['remote_option'] = forms.ChoiceField(
            choices=[
                ('onsite', 'On-site'),
                ('hybrid', 'Hybrid'),
                ('remote', 'Remote'),
            ],
            widget=forms.Select(attrs={'class': 'form-select'})
        )
        self.fields['employment_type'] = forms.ChoiceField(
            choices=[
                ('full_time', 'Full Time'),
                ('part_time', 'Part Time'),
                ('contract', 'Contract'),
                ('internship', 'Internship'),
                ('temporary', 'Temporary'),
            ],
            widget=forms.Select(attrs={'class': 'form-select'})
        )
        self.fields['experience_level'] = forms.ChoiceField(
            choices=[
                ('entry_level', 'Entry Level'),
                ('mid_level', 'Mid Level'),
                ('senior_level', 'Senior Level'),
                ('lead', 'Lead'),
                ('executive', 'Executive'),
            ],
            widget=forms.Select(attrs={'class': 'form-select'})
        )

    def clean(self):
        cleaned_data = super().clean()
        salary_min = cleaned_data.get('salary_min')
        salary_max = cleaned_data.get('salary_max')

        if salary_min is not None and salary_max is not None:
            if salary_min > salary_max:
                raise forms.ValidationError("Minimum salary cannot exceed maximum salary.")

        if salary_min is not None and salary_min < 0:
            raise forms.ValidationError("Salary cannot be negative.")

        if salary_max is not None and salary_max < 0:
            raise forms.ValidationError("Salary cannot be negative.")

        return cleaned_data