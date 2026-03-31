from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('alumni', 'Alumni'),
    )

    full_name    = models.CharField(max_length=100)
    email        = models.EmailField(unique=True)
    phone        = models.CharField(max_length=15, blank=True)
    role         = models.CharField(max_length=10, choices=ROLE_CHOICES)
    branch       = models.CharField(max_length=100, blank=True)
    profile_pic  = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio          = models.TextField(blank=True)
    is_verified  = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)
    otp            = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']

    def __str__(self):
        return f"{self.full_name} ({self.role})"


class StudentProfile(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_no        = models.CharField(max_length=15, blank=True)
    enrollment_no  = models.CharField(max_length=30, blank=True)
    current_year   = models.IntegerField(default=1)
    cgpa           = models.FloatField(default=0.0)
    github_url     = models.URLField(blank=True)
    linkedin_url   = models.URLField(blank=True)
    continuity_form = models.FileField(upload_to='continuity_forms/', blank=True, null=True)

    def __str__(self):
        return f"Student: {self.user.full_name}"
    
class AlumniProfile(models.Model):
    VERIFICATION_CHOICES = (
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    )

    user                = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alumni_profile')
    alumni_id           = models.CharField(max_length=50, blank=True)
    current_company     = models.CharField(max_length=100, blank=True)
    job_title           = models.CharField(max_length=100, blank=True)
    domain              = models.CharField(max_length=100, blank=True)
    graduation_year     = models.IntegerField(default=2020)
    experience_years    = models.IntegerField(default=0)
    github_url          = models.URLField(blank=True)
    linkedin_url        = models.URLField(blank=True)
    verification_status = models.CharField(max_length=10, choices=VERIFICATION_CHOICES, default='pending')

    def __str__(self):
        return f"Alumni: {self.user.full_name} - {self.current_company}"


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.full_name} - {self.name}"

class WorkExperience(models.Model):
    JOB_TYPE_CHOICES = (
        ('full-time', 'Full-time'),
        ('internship', 'Internship'),
        ('part-time', 'Part-time'),
        ('freelance', 'Freelance'),
    )

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_experiences')
    company     = models.CharField(max_length=100)
    role        = models.CharField(max_length=100)
    job_type    = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full-time')
    location    = models.CharField(max_length=100, blank=True)
    start_date  = models.DateField()
    end_date    = models.DateField(null=True, blank=True)
    is_current  = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    skills_used = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.user.full_name} - {self.role} at {self.company}"

    def duration(self):
        from datetime import date
        end = date.today() if self.is_current else self.end_date
        if end and self.start_date:
            months = (end.year - self.start_date.year) * 12 + (end.month - self.start_date.month)
            years = months // 12
            months = months % 12
            if years and months:
                return f"{years} yr {months} mos"
            elif years:
                return f"{years} yr"
            else:
                return f"{months} mos"
        return ""