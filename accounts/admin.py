from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, AlumniProfile, Skill

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    extra = 0

class AlumniProfileInline(admin.StackedInline):
    model = AlumniProfile
    can_delete = False
    extra = 0

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [StudentProfileInline, AlumniProfileInline]
    list_display = ['full_name', 'email', 'role', 'branch', 'is_verified', 'is_active']
    list_filter  = ['role', 'branch', 'is_verified', 'is_active']
    search_fields = ['full_name', 'email']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone', 'role', 'branch', 'bio', 'profile_pic')}),
        ('Permissions', {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password1', 'password2'),
        }),
    )

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'roll_no', 'enrollment_no', 'current_year', 'cgpa']
    search_fields = ['user__full_name', 'roll_no', 'enrollment_no']

@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_company', 'job_title', 'domain', 'graduation_year', 'verification_status']
    list_filter  = ['verification_status', 'domain']
    search_fields = ['user__full_name', 'current_company', 'alumni_id']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']
    search_fields = ['user__full_name', 'name']