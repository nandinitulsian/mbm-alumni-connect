from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, StudentProfile, AlumniProfile

class StudentRegisterForm(forms.ModelForm):
    roll_no = forms.CharField(
        label='Roll Number',
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. 22UECC8039'})
    )
    continuity_form = forms.FileField(
        label='Continuity Form (PDF)',
        required=True,
        widget=forms.FileInput()
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Create a password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'branch']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email':     forms.EmailInput(attrs={'placeholder': 'College email address'}),
            'phone':     forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'branch':    forms.TextInput(attrs={'placeholder': 'e.g. Computer Science'}),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don't match!")
        return p2

    def clean_continuity_form(self):
        file = self.cleaned_data.get('continuity_form')
        if file:
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed!")
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 5MB!")
        return file

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            StudentProfile.objects.create(
                user            = user,
                roll_no         = self.cleaned_data.get('roll_no', ''),
                continuity_form = self.cleaned_data.get('continuity_form'),
            )
        return user


class AlumniRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Create a password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'branch']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email':     forms.EmailInput(attrs={'placeholder': 'Your email address'}),
            'phone':     forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'branch':    forms.TextInput(attrs={'placeholder': 'e.g. Computer Science'}),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don't match!")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'alumni'
        user.is_verified = False
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            AlumniProfile.objects.create(user=user)
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Your email address'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Your password'})
    )


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['roll_no', 'enrollment_no', 'current_year', 'cgpa', 'github_url', 'linkedin_url', 'continuity_form']
        widgets = {
            'roll_no'       : forms.TextInput(attrs={'placeholder': 'e.g. 22UECC8039'}),
            'enrollment_no' : forms.TextInput(attrs={'placeholder': 'e.g. 0101CS22B039'}),
            'current_year'  : forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'cgpa'          : forms.NumberInput(attrs={'min': 0, 'max': 10, 'step': 0.1}),
            'github_url'    : forms.URLInput(attrs={'placeholder': 'https://github.com/username'}),
            'linkedin_url'  : forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/username'}),
        }


class AlumniProfileForm(forms.ModelForm):
    class Meta:
        model = AlumniProfile
        fields = ['alumni_id', 'current_company', 'job_title', 'domain', 'graduation_year', 'experience_years', 'github_url', 'linkedin_url']
        widgets = {
            'alumni_id'       : forms.TextInput(attrs={'placeholder': 'Alumni association ID'}),
            'current_company' : forms.TextInput(attrs={'placeholder': 'e.g. Google'}),
            'job_title'       : forms.TextInput(attrs={'placeholder': 'e.g. Software Engineer'}),
            'domain'          : forms.TextInput(attrs={'placeholder': 'e.g. SDE, Data Science, Finance'}),
            'graduation_year' : forms.NumberInput(attrs={'min': 1980, 'max': 2025}),
            'experience_years': forms.NumberInput(attrs={'min': 0, 'max': 50}),
            'github_url'      : forms.URLInput(attrs={'placeholder': 'https://github.com/username'}),
            'linkedin_url'    : forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/username'}),
        }

from .models import User, StudentProfile, AlumniProfile, WorkExperience

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model  = WorkExperience
        fields = ['company', 'role', 'job_type', 'location',
                  'start_date', 'end_date', 'is_current',
                  'description', 'skills_used']
        widgets = {
            'company'    : forms.TextInput(attrs={'placeholder': 'e.g. Google'}),
            'role'       : forms.TextInput(attrs={'placeholder': 'e.g. Software Engineer'}),
            'job_type'   : forms.Select(),
            'location'   : forms.TextInput(attrs={'placeholder': 'e.g. Bangalore'}),
            'start_date' : forms.DateInput(attrs={'type': 'date'}),
            'end_date'   : forms.DateInput(attrs={'type': 'date'}),
            'is_current' : forms.CheckboxInput(),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe your role and achievements...',
                'rows': 3
            }),
            'skills_used': forms.TextInput(attrs={'placeholder': 'e.g. Python, Django, SQL'}),
        }