from django import forms

from .models import Opportunity


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['company', 'role', 'type', 'domain', 'stipend', 'deadline', 'apply_link', 'description']
        widgets = {
            'company': forms.TextInput(attrs={'placeholder': 'e.g. Google'}),
            'role': forms.TextInput(attrs={'placeholder': 'e.g. Software Engineer Intern'}),
            'type': forms.Select(),
            'domain': forms.TextInput(attrs={'placeholder': 'e.g. SDE, Data Science, Finance'}),
            'stipend': forms.TextInput(attrs={'placeholder': 'e.g. 40,000/month or 12 LPA'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'apply_link': forms.URLInput(attrs={'placeholder': 'https://...'}),
            'description': forms.Textarea(attrs={'placeholder': 'Job description, requirements, etc.', 'rows': 5}),
        }
