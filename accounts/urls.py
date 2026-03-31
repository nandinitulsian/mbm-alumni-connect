from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/alumni/', views.register_alumni, name='register_alumni'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<int:user_id>/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('experience/add/', views.add_work_experience, name='add_work_experience'),
    path('experience/delete/<int:exp_id>/', views.delete_work_experience, name='delete_work_experience'),
]
