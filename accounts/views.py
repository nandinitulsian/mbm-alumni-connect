from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import StudentRegisterForm, AlumniRegisterForm, LoginForm, StudentProfileForm, AlumniProfileForm
from .models import User, StudentProfile, AlumniProfile, Skill
from connections.models import Connection
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def register_page(request):
    return render(request, 'accounts/register.html')

def register_student(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'
            user.is_active = False
            user.set_password(form.cleaned_data['password1'])
            user.otp = generate_otp()
            user.otp_created_at = timezone.now()
            user.save()
            StudentProfile.objects.create(
                user=user,
                roll_no=form.cleaned_data.get('roll_no', ''),
                continuity_form=form.cleaned_data.get('continuity_form'),
            )
            request.session['otp_user_id'] = user.id
            return redirect('verify_otp')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = StudentRegisterForm()
    return render(request, 'accounts/register_student.html', {'form': form})

def register_alumni(request):
    if request.method == 'POST':
        form = AlumniRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created! Please wait for admin verification.')
            return redirect('login')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = AlumniRegisterForm()
    return render(request, 'accounts/register_alumni.html', {'form': form})

def verify_otp(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        messages.error(request, 'Session expired. Please register again.')
        return redirect('register_student')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()
        otp_age = timezone.now() - user.otp_created_at
        if otp_age.seconds > 600:
            messages.error(request, 'OTP expired! Please register again.')
            user.delete()
            return redirect('register_student')
        if entered_otp == user.otp:
            user.is_active = True
            user.otp = None
            user.save()
            login(request, user)
            request.session.pop('otp_user_id', None)
            messages.success(request, f'Welcome {user.full_name}! Account verified!')
            return redirect('feed')
        else:
            messages.error(request, 'Wrong OTP! Please try again.')
    return render(request, 'accounts/verify_otp.html', {'user': user})

def resend_otp(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        return redirect('register_student')
    user = get_object_or_404(User, id=user_id)
    user.otp = generate_otp()
    user.otp_created_at = timezone.now()
    user.save()
    messages.info(request, 'New OTP generated!')
    return redirect('verify_otp')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.full_name}!')
            return redirect('feed')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

@login_required
def profile_view(request, user_id=None):
    if user_id:
        profile_user = get_object_or_404(User, id=user_id)
    else:
        profile_user = request.user

    student_profile = None
    alumni_profile  = None

    if profile_user.role == 'student':
        student_profile = StudentProfile.objects.filter(user=profile_user).first()
    else:
        alumni_profile = AlumniProfile.objects.filter(user=profile_user).first()

    skills = Skill.objects.filter(user=profile_user)
    from .models import WorkExperience
    work_experiences = WorkExperience.objects.filter(user=profile_user)

    # Get tab
    tab = request.GET.get('tab', 'posts')

    # Get posts based on tab
    from posts.models import Post, Like
    if tab == 'queries':
        posts = Post.objects.filter(
            author=profile_user,
            post_type='query'
        ).order_by('-created_at')
    elif tab == 'liked':
        liked_post_ids = Like.objects.filter(
            user=profile_user
        ).values_list('post_id', flat=True)
        posts = Post.objects.filter(
            id__in=liked_post_ids
        ).order_by('-created_at')
    else:
        posts = Post.objects.filter(
            author=profile_user
        ).order_by('-created_at')

    # Get connections
    from connections.models import Connection
    if profile_user.role == 'student':
        connections = Connection.objects.filter(
            student=profile_user,
            status='accepted'
        ).select_related('alumni', 'alumni__alumni_profile')
    else:
        connections = Connection.objects.filter(
            alumni=profile_user,
            status='accepted'
        ).select_related('student')

    connections_count = connections.count()

    return render(request, 'accounts/profile.html', {
    'profile_user'     : profile_user,
    'student_profile'  : student_profile,
    'alumni_profile'   : alumni_profile,
    'skills'           : skills,
    'is_own_profile'   : profile_user == request.user,
    'posts'            : posts,
    'tab'              : tab,
    'connections'      : connections,
    'connections_count': connections_count,
    'work_experiences' : work_experiences,
})
    
@login_required
def edit_profile(request):
    user = request.user
    if user.role == 'student':
        profile = StudentProfile.objects.filter(user=user).first()
        form_class = StudentProfileForm
    else:
        profile = AlumniProfile.objects.filter(user=user).first()
        form_class = AlumniProfileForm
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            skills_input = request.POST.get('skills', '')
            Skill.objects.filter(user=user).delete()
            for skill in skills_input.split(','):
                skill = skill.strip()
                if skill:
                    Skill.objects.create(user=user, name=skill)
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = form_class(instance=profile)
    skills = Skill.objects.filter(user=user)
    skills_str = ', '.join([s.name for s in skills])
    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'skills_str': skills_str,
    })

@login_required
def add_work_experience(request):
    if request.user.role != 'alumni':
        messages.error(request, 'Only alumni can add work experience!')
        return redirect('profile')

    from .forms import WorkExperienceForm
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            if exp.is_current:
                exp.end_date = None
            exp.save()
            messages.success(request, 'Work experience added!')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = WorkExperienceForm()
    return render(request, 'accounts/add_work_experience.html', {'form': form})

@login_required
def delete_work_experience(request, exp_id):
    from .models import WorkExperience
    exp = get_object_or_404(WorkExperience, id=exp_id, user=request.user)
    exp.delete()
    messages.success(request, 'Work experience deleted!')
    return redirect('profile')